import numpy as np
from functools import cmp_to_key


class matirx_solver:
    def __init__(self, graph):

        self.graph = graph # Adjacency matrix
        self.ppl = len(graph) # 200 to 216
        self.friends = len(graph[0]) # In this case will also be 200-216

    def bpm(self, u, matchR, seen):
        for v in range(self.friends):
            if self.graph[u][v] and seen[v] == False:
                seen[v] = True
                if matchR[v] == -1 or self.bpm(matchR[v],
                                               matchR, seen):
                    matchR[v] = u
                    return True
        return False

    def maxBPM(self):
        matchR = [-1] * self.friends
        result = 0
        for i in range(self.ppl):
            seen = [False] * self.friends
            if self.bpm(i, matchR, seen):
                result += 1
        return result, np.array(matchR)


def create_classes(results):
    # Class is used to pair two students that are friends with each other
    class pair:
        def __init__(self, students): # Students is array of length 2
            self.students = students
            # Stats recorded to be used when creating the classes
            self.male, self.female, self.islamic, self.native_arabic = 0, 0, 0, 0
            for student in self.students:
                if results[student][4] == 'M':
                    self.male += 1
                else:
                    self.female += 1
                self.islamic += results[student][2]
                self.native_arabic += results[student][3]

        # Get information about a student in pair. student argument can equal the index 0 or 1.
        def get_student(self, student):
            student_object = results[self.students[student]]
            return {'id': student_object[-1], 'gender': student_object[4], 'islamic': student_object[2],
                    'native_arabic': student_object[3]}

        def __str__(self):
            return f"Students: {self.students}, Males: {self.male}, Females: {self.female}, Islamic: {self.islamic}, native_arabic: {self.native_arabic}"

    # This class represents a classroom. Only 8 instances of this class is created
    class classroom:
        def __init__(self):
            # Record the students in the class and the statistics that can be displayed later
            self.students = []
            self.males = 0
            self.females = 0
            self.islamic = 0
            self.native_arabic = 0
            self.required = -1

        def __str__(self):
            return f'{self.students}, {self.males}, {self.females}, {self.islamic}, {self.native_arabic}'

        # Self explanatory - Adds a student to the classroom and updates the classroom's statistics
        def add_students(self, new_student):
            self.students.append(new_student)
            self.males += 1 if new_student['gender'] == 'M' else 0
            self.females += 1 if new_student['gender'] == 'F' else 0
            self.islamic += new_student['islamic']
            self.native_arabic += new_student['native_arabic']

    m = len(results)
    islamic, native_arabic, male, female = 0, 0, 0, 0

    for _ in range(m):
        for index in range(5, 10):
            if results[_][index] == _ + 1:
                if index == 5:
                    results[_][index] = results[_][index + 1]
                else:
                    results[_][index] = results[_][index - 1]
        islamic += 1 if results[_][2] == 1 else 0
        native_arabic += 1 if results[_][3] == 1 else 0
        if results[_][4] == 'M':
            male += 1
        else:
            female += 1

    if m == 200:
        students_per_class = [25] * 8
    elif m == 208:
        students_per_class = [26] * 8
    elif m == 216:
        students_per_class = [27] * 8
    elif 200 < m < 208:
        difference = m - 200
        students_per_class = []
        while difference >= 2:
            students_per_class.append(27)
            difference -= 2
        if difference == 1:
            students_per_class.append(26)
        if len(students_per_class) != 8:
            students_per_class += [25] * (8 - len(students_per_class))
    elif 208 < m < 216:
        difference = m - 208
        students_per_class = []
        while difference >= 1:
            students_per_class.append(27)
            difference -= 1
        if len(students_per_class) != 8:
            students_per_class += [26] * (8 - len(students_per_class))

    # Find mutual friends between the students
    mutuals = {}
    mutual_pairs = []
    used = []
    _ = 0
    while _ < m:
        for i in results[_][5:-1]:
            i -= 1
            if _ + 1 in results[i][5:-1] and _ not in used and i not in used:
                mutuals[_], mutuals[i] = i, _
                new_pair = pair([_, i])
                mutual_pairs.append(new_pair)
                used.append(_)
                used.append(i)
                break
        _ += 1

    adjacency_matrix = np.zeros([m, m])

    # Edits the adjacency matrix so that each student has value 1 for their friends
    for i in range(m):
        if i in used:
            adjacency_matrix[i, mutuals[i]] = 1
            continue
        for j in range(5, 10):
            if j - 1 in used:
                continue
            adjacency_matrix[i, results[i][j] - 1] = 1

    g = matirx_solver(adjacency_matrix)

    maximum_matchings, matchings = g.maxBPM()

    normal_pairs = []  # Initialize different data structures to help reduce time complexity
    lookup_pairs = {}  # because space complexity is not an issue.
    alone = []
    for _ in range(len(matchings)):
        if matchings[_] == _:
            alone.append(_)  # Check matches and if student matched with themselves, they are alone
            continue

        new_pair = pair([_, matchings[_]])  # Add matches to pair class
        normal_pairs.append(new_pair)
        lookup_pairs[new_pair.students[0]] = new_pair  # dictionary used to reduce time complexity with linear lookups.

    class_size = 8  # Create 8 classes total

    values = lookup_pairs.copy()
    ordered_pairs = []
    speciai_cases = []

    # Find dependencies in friends. i.e Bob has John as a friend while John has Marley as a friend
    # Here Bob, John and Marley are put in the same ordered pair so that they could all be with their friends.
    while len(values) > 0:
        index = list(values.keys())[0]
        to_add = values[index]
        del values[index]
        # Check if pair only has one student
        if to_add.students[1] == -1:
            speciai_cases.append(to_add)
        else:
            ordered_pairs.append(to_add)
            last_student = to_add.students[1]
            # Keep looping till values[last_student] does not exist
            while True:
                try:
                    to_add = values[last_student]
                except KeyError:
                    break
                del values[last_student]
                if to_add.students[1] == -1:
                    speciai_cases.append(to_add)
                    break
                ordered_pairs.append(to_add)
                last_student = to_add.students[1]

    # Code above leads to one long 1D array. Now a 2D array is created, where each index is
    # an array of students that all have their friends apart from one student (the last one)
    ordered_segments = []
    last = 0
    segment = []
    for x in ordered_pairs:
        if x.students[0] != last:
            ordered_segments.append(segment)
            segment = []
        segment.append(x)
        last = x.students[1]


    def get_distribution(students):
        males, females, total_islamic, total_native_arabic = 0, 0, 0, 0
        for student in students:
            if student['gender'] == 'M':
                males += 1
            else:
                females += 1
            total_islamic += student['islamic']
            total_native_arabic += student['native_arabic']
        return males, females, total_islamic, total_native_arabic

    # Custom key to sort the scores based on cost
    def sort_by_cost(a, b):
        if a[0] >= b[0]:
            return 1
        return -1

    def get_cost(students):  # Cost function is called upon to get a number for how balanced a group of students are
        if len(students) == 0:
            return 0.0, []
        # Get_distribution is a function that loops through students and returns that statistics of that group.
        males, females, total_islamic, total_native_arabic = get_distribution(students)
        cost = (2 / 3 * abs(males - females) + 1 / 3 * (total_islamic + total_native_arabic)) / (males + females)
        return cost, [males, females, total_islamic, total_islamic]

    not_used_class_sizes = []
    for _ in students_per_class:
        not_used_class_sizes.append(_)

    def split_equally(students, force_split=False):  # Function used to split ordered_segments into smaller pieces if longer than 6 or not balanced
        cost_parent, details_parent = get_cost(students)
        if cost_parent <= 0.3 and len(students) in not_used_class_sizes and not force_split:  # If segment is balanced, not need to split it
            del not_used_class_sizes[not_used_class_sizes.index(len(students))]
            return [students], []
        elif ((cost_parent <= 0.3 and len(students) < min(not_used_class_sizes)) or len(students) < 6) and not force_split:
            return [students], []
        else:
            min_size = 2  # Segment cannot be less than 2
            cyclic_array = students[1:] + students  # Cyclic array with center being students[0]
            length = len(students)
            scores = []
            left = 0
            right = length
            while right != len(cyclic_array): # All possible splits are made and their cost is calculated.
                while right - left != min_size:
                    index = [left, right]
                    remaining_array = []
                    for student in students:
                        if student not in cyclic_array[left:right]:
                            remaining_array.append(student)
                    cost, details = get_cost(cyclic_array[left:right])
                    cost_other, details_other = get_cost(remaining_array)
                    scores.append(
                        [(cost * len(cyclic_array[left:right]) + cost_other * len(remaining_array)) / length, index,
                         details, details_other])
                    right -= 1
                left += 1
                right = length + left
            scores.sort(key=cmp_to_key(sort_by_cost))
            lowest_cost = scores[0][0]
            to_consider = []
            for score in scores:
                if score[0] == lowest_cost:  # Usually multiple splits have the same cost so they are all considered
                    to_consider.append(score)
                else:
                    break
            current_best, current_best_length_diff = None, None
            # From to_consider, the split that has both parts most balanced will be used.
            # (i.e split from 10 to 5,5 is better than 9,1)
            for score in to_consider:
                indicies = score[1]
                score_diff_between_lengths = abs(
                    (indicies[1] - indicies[0]) - (len(students) - (indicies[1] - indicies[0])))
                if current_best is None or score_diff_between_lengths < current_best_length_diff:
                    current_best, current_best_length_diff = score, score_diff_between_lengths

            best_split = current_best
            if not force_split:
                # Check if new split is more optimal than the original sequence.
                if best_split[0] > cost_parent and len(students) <= students_per_class:
                    return [students], []
            left, right = best_split[1][0], best_split[1][1]
            array_found = cyclic_array[left:right]  # One part of the split
            array_remaining = []  # Other part of the split
            for student in students:
                if student not in array_found:
                    array_remaining.append(student)
            if len(array_remaining) == 0:
                return [students], []

            left = array_found
            right = array_remaining
            segs = []
            friend_lost = [cyclic_array[best_split[1][0] - 1]]
            #return [left, right], friend_lost
            test_left = split_equally(left)
            for _ in test_left[0]:
                segs.append(_)
            for _ in test_left[1]:
                friend_lost.append(_)
            test_right = split_equally(right)
            for _ in test_right[0]:
                segs.append(_)
            for _ in test_right[1]:
                friend_lost.append(_)

            return segs, friend_lost

    total = 0
    split_segments = []
    students_with_no_friends = []
    for s in ordered_segments:
        s_students = [x.get_student(0) for x in s]
        if len(s_students) < 6:
            total += len(s_students)
            if len(s_students) == 1:
                alone.append(s_students[0])

            split_segments.append(s_students)
            continue
        if s[0].students[0] != s[-1].students[1]:
            students_with_no_friends.append(s[-1].get_student(0))
        segments, no_friends = split_equally(s_students)
        for student_alone in no_friends:
            if student_alone not in students_with_no_friends:
                students_with_no_friends.append(student_alone)

        for x in segments:
            total += len(x)
            split_segments.append(x)

    single_people = []
    for x in speciai_cases:
        single_people.append(x.get_student(0))
        split_segments.append([x.get_student(0)])

    split_segments.extend(single_people)

    def sort_based_on_length(a, b):
        if len(a) <= len(b):
            return 1
        return -1

    split_segments.sort(key=cmp_to_key(sort_based_on_length))

    classes = []
    for _ in range(class_size):
        classes.append(classroom())
        classes[_].required = students_per_class[_]
    filled_classes = []


    used = 0

    for i in range(len(split_segments)):
        if i >= class_size:
            break
        for student in split_segments[0]:
            used += 1
            classes[i].add_students(student)
        del split_segments[0]


    while len(classes) != 0 and len(split_segments) != 0:

        for t in range(len(split_segments)):
            x = split_segments[t]
            too_big = 0
            for j in classes:
                if len(x) > j.required-len(j.students):
                    too_big += 1
            if too_big >= len(classes):
                if len(x) < 5:
                    for l in range(len(x)):
                        for stu in x:
                            split_segments.append(stu)
                    del split_segments[t]
                else:
                    new = split_equally(x, force_split=True)
                    del split_segments[t]
                    for segm in new[0]:
                        split_segments.append(segm)

        i = 0
        while i < len(classes):
            students_required = classes[i].required - len(classes[i].students)
            for x in range(len(split_segments)):
                if type(split_segments[x]) is dict:
                    split_segments[x] = [split_segments[x]]
                if len(split_segments[x]) <= students_required:
                    for student in split_segments[x]:
                        used += 1
                        classes[i].add_students(student)
                    students_required -= len(split_segments[x])
                    del split_segments[x]
                    break
            if students_required <= 0: # Makes sure it is filled fully
                filled_classes.append(classes[i])
                del classes[i]
                i -= 1
            i += 1


    return filled_classes, students_with_no_friends+alone, {'Males': male, 'Females': female, 'Islamic Students': islamic, 'Native Arabic Students': native_arabic}

