from django.shortcuts import render, redirect, reverse, HttpResponse
from django.contrib import messages
import csv, re, zipfile
from .forms import Student_form
from .models import Student
from io import StringIO, BytesIO


def home(request):
    return render(request, 'home.html')


def process(request, grade):
    # Run the create_classes algorithm that is called by distribute_to_classes after it parses all the data from the database into a 2D array.
    classes, students_with_no_friends, overview = Student.distribute_to_classes(grade)
    # If any 'class X' button was pressed, POST request was made.
    if request.method == 'POST':
        class_number = int(list(request.POST.keys())[1])  # Get class number from form in previous page
        current_class = classes[class_number-1]  # Index is always one less
        students = []
        # Get students' full information from database via their ID
        for student in current_class.students:
            data = Student.objects.filter(id=student['id']).values('powerschool_id', 'first_name',
                                                                   'last_name', 'gender',
                                                                   'arabic', 'islamic')
            students_friends = []
            # Gets the friends_unprocessed column of student and then converts it into array by replacing more than one space with a split to create array.
            students_friends_expected = re.split(r'\s{2,}', list(Student.objects.filter(id=student['id']).values('friends_unprocessed')[0].values())[0])
            # Loop to see if any people in class are friend of the student.
            for i in current_class.students:
                name = ' '.join(list(Student.objects.filter(id=i['id']).values('first_name', 'last_name')[0].values()))
                if name in students_friends_expected:
                    students_friends.append(name)
            # If student has at least one friend, give check mark status near name
            if len(students_friends) != 0:
                status = ['<i class="fa fa-check-circle" style="font-weight: 900"></i>' ]
            # Else warning sign
            else:
                status = ['<i class="fa fa-warning" style="font-weight: 900; color: #d9534f"></i>']
            students_friends = [', '.join(students_friends) if len(students_friends) != 0 else 'None']  # Format friends list nicely
            students.append(status+list(data[0].values())+students_friends)
        context = {
            'grade': grade,
            'class_number': class_number,
            'Students': students,
            'overview': {'Males': current_class.males, 'Females': current_class.females,
                         'Islamic Students': current_class.islamic, 'Native Arabic Students': current_class.native_arabic},
            'url_back': reverse('organized', kwargs={"grade":grade})
        }

        return render(request, 'class_stats.html', context)

    num_of_classes = range(1, len(classes)+1)
    processed_num_classes = []
    for i in range(0, len(num_of_classes), 4):
        processed_num_classes.append(num_of_classes[i:i + 4])  # Create two arrays of four classes

    context = {
        'classes': classes,
        'num_classes': processed_num_classes,
        'overview': overview,
        'grade': grade,
        'url_back': reverse('homepage')
    }
    return render(request, 'schedule.html', context)

def grade_no_friends(request, grade):
    classes, students_with_no_friends, overview = Student.distribute_to_classes(grade)

    student_to_class = {}

    for i in range(len(classes)):
        cls = classes[i]
        for student in cls.students:
            student_to_class[student['id']] = i+1

    final_no_friends = []


    for student in students_with_no_friends:
        # SINCE ERROR SKIP MISSING KIDS
        try:
            data = Student.objects.filter(id=student['id']).values('powerschool_id', 'first_name',
                                                                   'last_name', 'gender',
                                                                   'arabic', 'islamic')
            results = list(data[0].values())+[student_to_class[student['id']]]
            final_no_friends.append(results)
        except:
            pass


    context = {
        'grade': grade,
        'no_friends': final_no_friends,
        'url_back': reverse('organized', kwargs={"grade":grade})
    }
    return render(request, 'grade_no_friends.html', context)


def upload(request, grade):
    '''
    The user can upload a:
    - CSV file
    - A form

    This data is processed an put into the mySQL database
    '''

    # Reset a csv reader
    def reset_csv(string_io, data):
        string_io.close()
        string_io = StringIO(data)
        return csv.reader(string_io, delimiter=',')

    # Formats names to reduce errors with capitalization
    def format(name):
        return name.lower().title()

    # Check if DB already has students 200+ students
    if len(Student.objects.filter(grade=grade)) >= 200:
        return redirect(reverse('organized', kwargs={"grade":grade}))

    context = {
        'url_back': reverse('homepage')
    }

    if request.method == 'GET':
        return render(request, 'upload_data.html', context)

    # Check if user uploads a file
    if 'file_submission' in request.POST:
        # Check if the file is of type csv
        try:
            csv_file = request.FILES['file']
        except:
            messages.error(request, "Please choose a file")
            return render(request, 'upload_data.html', context)
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'This is not a csv file')
            return render(request, 'upload_data.html', context)

        # If it is a CSV file, process it
        data = csv_file.read().decode('UTF-8')
        io_string = StringIO(data)
        csv_reader = csv.reader(io_string, delimiter=',')

        # Check that columns required are included
        columns = next(csv_reader)

        expected = ["Powerschool ID", "First Name", "Last Name", f"Grade {grade-1}", "Gender", "Social Grouping", "ARABIC NATIVE/NON NATIVE", "ISLAMIC NATIVE/NON NATIVE", "Nationality", "ELL", "SEND", "Behavior", "HMP", "H/L", "Friends", "Avoid", "Additional Notes"]

        if len(columns) != len(expected):
            msg = "The CSV file uploaded does not have the required columns"
            ## SHOW THE REQUIRED COLUMNS
            messages.error(request, msg)
            return render(request, 'upload_data.html', context)

        for i in range(len(columns)):
            if format(expected[i]) not in format(columns[i]):
                msg = "The CSV file uploaded does not have the required column names, which may mean different data has been entered. Expected columns:"
                messages.error(request, msg)
                msg = f'"Powerschool ID", "First Name", "Last Name", "Grade {grade-1}", "Gender", "Social Grouping", "ARABIC NATIVE/NON NATIVE", "ISLAMIC NATIVE/NON NATIVE", "Nationality", "ELL", "SEND", "Behavior", "HMP", "H/L", "Friends", "Avoid", "Additional Notes"'
                messages.error(request, msg)
                return render(request, 'upload_data.html', context)

        number_of_rows = len(list(csv_reader))
        if number_of_rows < 200 or number_of_rows > 216:
            msg = "There are not enough or too many students in the CSV file. Please add make sure there is between 200 to 216 students and reupload."
            messages.error(request, msg)
            return render(request, 'upload_data.html', context)

        # Since data valid, delete previous data in DB
        Student.objects.filter(grade=grade).delete()

        # Reset csv reader
        csv_reader = reset_csv(io_string, data)

        # Loop through all the students and save them to the database
        id_for_students = {"N/A":-1}
        next_free_id = 0

        # Get ID for each student
        for row in csv_reader:
            id_for_students[format(row[1]) + " " + format(row[2])] = next_free_id
            next_free_id += 1

        # Reset csv reader
        csv_reader = reset_csv(io_string, data)

        columns = next(csv_reader)

        for row in csv_reader:
            # Check the data is valid
            fails = 0
            fails += 0 if bool(re.match("^[0-9]*$", row[0])) else 1
            fails += 0 if bool(re.match("^[A-Za-z ]*$", row[1] + " " + row[2])) else 1
            fails += 0 if bool(re.match("^[A-Za-z]*$", row[4])) else 1
            fails += 0 if bool(re.match("^[A-Za-z]*$", row[6])) else 1
            fails += 0 if bool(re.match("^[A-Za-z]*$", row[7])) else 1
            fails += 0 if bool(re.match("^[A-Za-z ]*$", row[14])) else 1

            # If data not valid, send error message
            if fails != 0:
                msg = f"There has been a formatting issue with the student {row[1]} {row[2]}. Please check their information and make sure it is all correct."
                messages.error(request, msg)
                return render(request, 'upload_data.html', context)

            # Save the model with student data
            islamic_status = 'N' if row[7] == 'N' else 'NN' if row[7] == 'NN' else 'None'
            friends = re.split(r'\s{2,}', row[14])
            if len(friends) != 5:
                to_add_null = 5-len(friends)
                for _ in range(to_add_null):
                    friends.append("N/A")
            # Change names of friends to ID.
            for i in range(len(friends)):
                try:
                    friends[i] = id_for_students[format(friends[i])]
                except:
                    msg = f"{friends[i]} is one of {format(row[1] + ' ' + row[2])}'s friends, but they are not in the CSV file uploaded. Please add this student and reupload."
                    messages.error(request, msg)
                    return render(request, 'upload_data.html', context)

            # Save info to Student model
            student = Student(
                powerschool_id=row[0],
                first_name=format(row[1]),
                last_name=format(row[2]),
                previous_grade=row[3],
                grade=grade,
                gender=row[4],
                social_grouping=row[5],
                arabic=row[6],
                islamic=islamic_status,
                takes_native_arabic=False if row[6] == 'NN' else True,
                takes_islamic=False if islamic_status == 'None' else True,
                nationality=row[8],
                ell='Y' if row[9] =='Y' else 'N',
                send='Y' if row[10] =='Y' else 'N',
                behavior=row[11],
                hmp=row[12],
                hORl='H' if row[13] == 'H' else 'L' if row[13] == 'L' else 'N',
                friend1=friends[0],
                friend2=friends[1],
                friend3=friends[2],
                friend4=friends[3],
                friend5=friends[4],
                friends_unprocessed=row[14],
                avoid=row[15],
                notes=row[16]
            )

            student.save()

    # Once finished, redirect to the home page
    return redirect(reverse("class", kwargs={"grade":grade}))


def reset_data(request, grade):
    Student.objects.filter(grade=grade).delete()
    return redirect(reverse("homepage"))


def download_file(request, grade, class_number):
    classes, students_with_no_friends, overview = Student.distribute_to_classes(grade)

    # Check if user wants to export all of the classes (101). If single class, then 0 < class_number < 9
    if class_number == 101:
        classes_data = []
        for class_num in range(1,9):
            # StringIO will listen and record all the data written to 'writer'.
            class_io = StringIO()
            writer = csv.writer(class_io)

            writer.writerow([f"Class: {grade}.{class_num}", "Powerschool ID", "First Name", "Last Name", "Gender",
                             "ARABIC NATIVE/NON NATIVE", "ISLAMIC NATIVE/NON NATIVE", f"Grade {grade - 1} - Former",
                             "Nationality", "ELL", "SEND", "Behavior", "HMP", "H/L", "Friends", "Avoid",
                             "Additional Notes"])
            # get data from database or from text file....
            temp = classes[class_num - 1]
            students_to_save = []

            for val in temp.students:
                students_to_save.append(val['id'])

            data_to_save = Student.objects.filter(grade=grade).values("id", "powerschool_id", "first_name", "last_name",
                                                                      "gender", "arabic", "islamic", "previous_grade",
                                                                      "nationality", "ell", "send", "behavior", "hmp",
                                                                      "hORl", "friends_unprocessed", "avoid", "notes")
            # Add data to the writer for each student in class
            for student in data_to_save:
                if student['id'] in students_to_save:
                    data = list(student.values())[1:]
                    writer.writerow([''] + data)
                else:
                    continue

            classes_data.append(class_io.getvalue().strip('\r\n'))

        # ByteIO and not StringIO because zipfile does not output string but rather bytes
        output = BytesIO()
        f = zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED)
        for _ in range(8):
            f.writestr(f"Grade {grade} Classroom {_+1} Students.csv", classes_data[_])
        f.close()
        # Send response to website with the ZIP file
        response = HttpResponse(output.getvalue(), content_type='text/zip')
        response['Content-Disposition'] = f'attachment; filename="Grade {grade} Classes.zip"'
    else:
        # StringIO will listen and record all the data written to 'writer'.
        class_io = StringIO()
        writer = csv.writer(class_io)

        writer.writerow([f"Class: {grade}.{class_number}", "Powerschool ID", "First Name", "Last Name", "Gender", "ARABIC NATIVE/NON NATIVE",
                         "ISLAMIC NATIVE/NON NATIVE", f"Grade {grade-1} - Former", "Nationality", "ELL", "SEND",
                         "Behavior", "HMP", "H/L", "Friends", "Avoid", "Additional Notes"])
        # get data from database or from text file....
        temp = classes[class_number-1]
        students_to_save = []

        for val in temp.students:
            students_to_save.append(val['id'])

        data_to_save = Student.objects.filter(grade=grade).values("id", "powerschool_id", "first_name", "last_name", "gender",
                                                                  "arabic", "islamic", "previous_grade", "nationality", "ell",
                                                                  "send", "behavior", "hmp", "hORl", "friends_unprocessed", "avoid",
                                                                  "notes")
        # Add data to the writer for each student in class
        for student in data_to_save:
            if student['id'] in students_to_save:
                data = list(student.values())[1:]
                writer.writerow([''] + data)
            else:
                continue

        # response content type
        response = HttpResponse(class_io.getvalue(), content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="Grade {grade} Classroom {class_number} Students.csv"'
    return response