import pandas as pd
import csv
import string
import random
import numpy as np
import pathlib
from faker import Faker
from unidecode import unidecode

path = str(pathlib.Path(__file__).parent.resolve())+'\\binaries\\'
fake = Faker('el_GR')

entities_properties = {
    'Client': {"Client_ID": ['integer', True], "Firstname": ['text', False], "Surname": ['text', False], "Discount": ['float', False], "City": ['text', False],
               "Addr": ['text', False], "Postcode": ['text', False], "IP": ['text', False], "Phone_number": ['text', False], "Email": ['text', False],
               "Birth_date": ['date', False], "Join_date": ['date', False], "IBAN": ['text', False]},

    'Employee': {"Employee_ID": ['integer', True], "Firstname": ['text', False], "Surname": ['text', False], "Salary": ['integer', False], "Phone_number": ['text', False],
                 "Birth_date": ['date', False]},

    'Partner': {"Partner_ID": ['integer', True], "Firstname": ['text', False], "Surname": ['text', False], "Phone_number": ['text', False], "Addr": ['text', False],
                "TIN": ['integer', False, True], "IBAN": ['text', False], "Representative": ['text', False]},

    'Informs': {"Inform_ID": ['integer', True], "Information": ['text', False], "Creation_date": ['date', False],
                "Creator": ['integer', False, 'Employee', 'Employee_ID'], "Recipiant": ['integer', False, 'Employee', 'Employee_ID']},

    'Recommendation': {"Recommendation_ID": ['integer', True], "Information": ['text', False],
                       "Recommender": ['integer', False, 'Client', 'Client_ID'], "Recommended": ['integer', False, 'Client', 'Client_ID'],
                       "Date": ['date', False]},

    'Category': {"Category_ID": ['integer', True], "Genre": ['text', False, True], "Targeted_Audience": ['text', False]},

    'Writer': {"Partner_ID": ['integer', True, 'Partner', 'Partner_ID'], "Specialization_category": ['integer', False, 'Category', 'Category_ID'], "Education": ["text", False],
               "CV": ['binary', False]},

    'Printing_Facility': {"Partner_ID": ['integer', True, 'Partner', 'Partner_ID'], "Facility_type": ['text', False],
                          "Capabilities": ['text', False]},

    'Contract': {"Contract_ID": ['integer', True], "Writer": ['integer', False, 'Writer', 'Partner_ID'], "Immidiate_payment": ['float', False],
                 "Percentage_on_sales": ['float', False], "Initial_PDF": ['binary', False], 'Sign_date': ['date', False], "Copyrights": ['text', False],
                 "Responsible_employee": ['integer', False, 'Employee', 'Employee_ID']},

    'Book': {"Book_ID": ['integer', True], "ISBN": ['text', False, True], "Category": ['integer', False, 'Category', 'Category_ID'], "Multimedia": ['binary', False],
             "Avail": ['integer', False], "Pages": ['integer', False], "Writer": ['integer', False, 'Writer', 'Partner_ID'], "Book_weight": ['float', False],
             "Dimensions": ['text', False]},

    'Batch': {"Batch_number": ['integer', True], "Book": ['integer', False, 'Book', 'Book_ID'], "Quantity": ['integer', False],
              "Cost": ['float', False], "Start_date": ['date', False], "End_date": ['date', False],
              "Contract_ID": ['integer', False, 'Contract', 'Contract_ID'], "Final_PDF": ['binary', False]},

    'Production_Action': {"Action_ID": ['integer', True], "Batch_number": ['integer', False, 'Batch', 'Batch_number'],
                          "Cost": ['float', False], "Action_type": ['text', False], "Details": ['text', False],
                          "Responsible_Employee": ['integer', False, 'Employee', 'Employee_ID'],
                          "Producer_ID": ['integer', False, 'Printing_Facility', 'Partner_ID']},

    'Purchase': {"Purchase_ID": ['integer', True], "Client": ['integer', False, 'Client', 'Client_ID'],
                 "Responsible_Employee": ['integer', False, 'Employee', 'Employee_ID'], "Book": ['integer', False, 'Book', 'Book_ID'],
                 "Count": ['integer', False], "Cost": ['float', False], "Total_weight": ['float', False], "Total_volume": ['text', False],
                 "Details": ['text', False], "Purchase_date": ['date', False], "Pr_level": ['integer', False]}
}


def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def get_random_binary(length):
    result_str = ''.join(random.choice([0, 1]) for i in range(length*8))
    return result_str


def get_relevant(entity, attribute):
    df = pd.read_csv("{}.csv".format(entity))
    saved_column = df[attribute]
    return list(saved_column)


def make_1(leksiko, entity):

    discounts = np.arange(start=0.1, stop=0.8, step=0.1)
    primaryKey = 1
    entity_diction = leksiko[entity]
    list_of_dicts = []
    primaries = []
    if entity=='Partner':
        end=25 #must be bigger than printing facilities+writers (this is partner)
    elif entity=='Employee':
        end=15
    else:
        end = random.randint(60, 90)
    for i in range(1, end):
        temp_dict = {}
        for attribute in entity_diction.keys():
            typos = entity_diction[attribute][0]
            primary = entity_diction[attribute][1]
            name = attribute
            if primary == False:
                if typos == 'integer':
                    if name == 'TIN':
                        temp_dict[name] = fake.unique.ssn()
                    elif name == 'Salary':
                        temp_dict[name] = random.randint(1000, 2000)

                elif typos == 'text':
                    if name == 'Firstname':
                        if i % 2:
                            fname = fake.first_name_female()
                        else:
                            fname = fake.first_name_male()
                        temp_dict[name] = fname
                    elif name == 'Surname':
                        if i % 2:
                            sname = fake.last_name_female()
                        else:
                            sname = fake.last_name_male()
                        temp_dict[name] = sname
                    elif name == 'Addr':
                        temp_dict[name] = fake.street_address()
                    elif name == 'City':
                        temp_dict[name] = fake.city()
                    elif name == 'Postcode':
                        temp_dict[name] = fake.postcode()
                    elif name == 'IP':
                        temp_dict[name] = fake.ipv4()
                    elif name == 'Phone_number':
                        temp_dict[name] = fake.phone_number()
                    elif name == 'IBAN':
                        temp_dict[name] = fake.iban()
                    elif name == 'Email':
                        temp_dict[name] = unidecode(
                            fname).lower() + unidecode(sname).lower() + '@gmail.com'
                    elif name == 'Representative':
                        temp_dict[name] = fake.first_name() + ' ' + \
                            fake.last_name()

                elif typos == 'float':
                    if name == 'Discount':
                        temp_dict[name] = round(
                            discounts[random.randint(0, 6)], 2)

                elif typos == 'date':
                    if name == 'Birth_date':
                        birth_date = fake.date_of_birth(
                            minimum_age=18, maximum_age=100).strftime("%Y-%m-%d")
                        temp_dict[name] = birth_date
                    else:
                        temp_dict[name] = fake.date_between(start_date='-10y')
                else:
                    print('error   ', typos, entity)

            if primary == True:
                while True:
                    temp = primaryKey
                    primaryKey += 1
                    if temp not in primaries:
                        temp_dict[name] = temp
                        primaries.append(temp)
                        break
        list_of_dicts.append(temp_dict)
        with open('{}.csv'.format(entity), 'w', encoding='utf8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=entity_diction.keys())
            writer.writeheader()
            writer.writerows(list_of_dicts)
    return primaries


def make_2(leksiko, entity, primars):

    informs = ['Αύριο στις 11 \n      γενική συνάντηση', 'Πάρε άμεσα το αφεντικό',
               'Η παρουσίαση θα γίνει \n         την Παρασκευή', 'Ένας συγγραφέας θα \n       περάσει το απόγευμα για συμβόλαιο']
    recommends = ['Ο καλύτερος εκδοτικός \n       οίκος της δεκαετίας', 'Αξεπέραστη \n       ποιότητα βιβλίων',
                  'Εξαιρετικά φιλικοί \n       με τους πελάτες', 'Επιλέγουν σοφά \n       τους συγγραφείς τους']
    genres = ['Φαντασίας', 'Επιστημονικής φαντασίας', 'Δυστοπικά', 'Δράσης και περιπέτειας', 'Μυστηρίου', 'Θρίλερ', 'Αστυνομικά', 'Ιστορικής φαντασίας',
              'Ρομαντικά', 'Μικρού μήκους', 'Σύγχρονης φαντασίας', 'Φιλοσοφικά', 'Νουβέλες', 'Γραφικά',
              'Εφηβικά', 'Νεανικά ', 'Παιδικά', 'Αυτοβιογραφίες', 'Θεολογικά', 'Τέχνης', 'Ιστορικά', 'Αληθινά εγκλήματα', 'Σατιρικά',
              'Επιστημονικά', 'Κοινωνικών επιστημών', 'Ακαδημαϊκά', 'Τεχνολογίας', 'Ταξίδια και Φαγητό']
    education = ['Λύκειο', 'Πανεπιστήμιο', 'Μεταπτυχιακό', 'Διδακτορικό']
    dimensions = ['30 x 48', '17 x 23  ', '15 x 23 ', '10 x 17 ']
    action_details_supply = [
        'Αναμένεται καθυστέρηση λόγω \n       προβλημάτων στη εφοδιαστική αλυσίδα', 'Αναμένεται εντός του μήνα']
    action_details_print = [
        'Αναμένεται καθυστέρηση λόγω\n       βλάβης εκτυπωτή', 'Η εκτύπωση ξεκινά από αύριο']
    purchase_details = ['1ος όροφος', 'Λείπει τα Σ/Κ',
                        'Διαθέσιμος για παραλαβή \n        από Δευτέρα', 'Στείλτε όλη την \n       παρτίδα σε μια αποστολή']
    copyrights = ['All rights reserved',
                  'Some rights reserved', 'No rights reserved']
    action_type = ["Προμήθεια", "Εκτύπωση"]
    volumes = ['1x2x3', '1x1x1', '2x2x2', '0.2x0.2x0.1']
    percentage_on_sales = np.arange(start=0.1, stop=0.5, step=0.05)
    immediate_payments = [1000.0, 2000.0, 3000.0, 8000.0]
    book_weights = [0.2, 0.8, 1.5, 2.2]
    total_weights = [2, 10, 30, 1200]
    locs = ['senario1.txt', 'senarioxionaths.txt', 'senariostaxtopoutas.txt']
    avails = [200, 40, 400, 1800]
    pages = [20, 50, 600, 1050]
    quantities = [20, 50, 200, 800]
    count = [8, 80, 800, 1800]
    pr_levels = [1, 2, 3, 4]
    targeted_audieces = ['Παιδιά', 'Έφηβοι',
                         'Φοιτητές', 'Ενήλικες', 'Γονείς', 'Γυναίκες', 'Άντρες']
    primaryKey = 1
    entity_diction = leksiko[entity]
    list_of_dicts = []
    primaries = []
    end = random.randint(35, 75)
    if entity=='Category':
        end=15
    if entity=='Contract':
        end=37
    if entity=='Batch':
        end=47
    if entity=='Production_Action':
        end=74
    if entity=='Purchase':
        end=random.randint(120, 350)
    for i in range(1, end):
        temp_dict = {}
        for attribute in entity_diction.keys():
            typos = entity_diction[attribute][0]
            primary = entity_diction[attribute][1]
            name = attribute
            if len(entity_diction[attribute]) < 4:
                if primary == False:
                    if typos == 'integer':
                        if name == 'Avail':
                            temp_dict[name] = avails[random.randint(0, 3)]
                        elif name == 'Pages':
                            temp_dict[name] = pages[random.randint(0, 3)]
                        elif name == 'Quantity':
                            temp_dict[name] = quantities[random.randint(0, 3)]
                        elif name == 'Count':
                            temp_dict[name] = count[random.randint(0, 3)]
                        elif name == 'Pr_level':
                            temp_dict[name] = pr_levels[random.randint(0, 3)]
                    elif typos == 'text':
                        if name == 'Genre' and i < len(genres):
                            temp_dict[name] = genres[i]
                        elif name == 'Targeted_Audience':
                            temp_dict[name] = targeted_audieces[random.randint(
                                0, 6)]
                        elif name == 'Information' and entity == 'Informs':
                            temp_dict[name] = informs[random.randint(0, 3)]
                        elif name == 'Information' and entity == 'Recommendation':
                            temp_dict[name] = recommends[random.randint(0, 3)]
                        elif name == 'Education':
                            temp_dict[name] = education[random.randint(0, 3)]
                        elif name == 'Copyrights':
                            temp_dict[name] = copyrights[random.randint(0, 2)]
                        elif name == 'Dimensions':
                            temp_dict[name] = dimensions[random.randint(0, 3)]
                        elif name == 'ISBN':
                            temp_dict[name] = fake.unique.isbn10()
                        elif name == 'Action_type':
                            act_type = action_type[random.randint(0, 1)]
                            temp_dict[name] = act_type
                        elif name == 'Details' and entity == 'Production_Action':
                            if act_type == 'Προμήθεια':
                                temp_dict[name] = action_details_supply[random.randint(
                                    0, 1)]
                            elif act_type == 'Εκτύπωση':
                                temp_dict[name] = action_details_print[random.randint(
                                    0, 1)]
                        elif name == 'Details' and entity == 'Purchase':
                            temp_dict[name] = purchase_details[random.randint(
                                0, 3)]
                        elif name == 'Total_volume':
                            temp_dict[name] = volumes[random.randint(0, 1)]
                        else:
                            temp_dict[name] = get_random_string(
                                random.randint(1, 64))
                    elif typos == 'float':
                        if name == 'Percentage_on_sales':
                            temp_dict[name] = round(percentage_on_sales[random.randint(
                                0, 7)], 2)
                        elif name == 'Immidiate_payment':
                            temp_dict[name] = immediate_payments[random.randint(
                                0, 3)]
                        elif name == 'Book_weight':
                            temp_dict[name] = round(book_weights[random.randint(
                                0, 3)], 2)
                        elif name == 'Cost':
                            temp_dict[name] = round(
                                random.uniform(10.00, 2000.00), 2)
                        elif name == 'Total_weight':
                            temp_dict[name] = round(total_weights[random.randint(
                                0, 3)], 2)
                        else:
                            temp_dict[name] = round(1/random.randint(1, 15), 2)

                    elif typos == 'date':
                        temp_dict[name] = fake.date()

                    elif typos == 'binary':
                        temp_dict[name] = "\n" + \
                            str(path+locs[random.randint(0, 2)])

                else:
                    while True:
                        temp = primaryKey
                        primaryKey += 1
                        if temp not in primaries:
                            temp_dict[name] = temp
                            primaries.append(temp)
                            break
            elif len(entity_diction[attribute]) == 4:
                if primary == True:
                    while True:
                        temp = random.choice(get_relevant(
                            entity_diction[attribute][2], entity_diction[attribute][3]))
                        if temp not in primaries:
                            temp_dict[name] = temp
                            primaries.append(temp)
                            break
                else:
                    temp_dict[name] = random.choice(get_relevant(
                        entity_diction[attribute][2], entity_diction[attribute][3]))

        list_of_dicts.append(temp_dict)
        with open('{}.csv'.format(entity), 'w', encoding='utf8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=entity_diction.keys())
            writer.writeheader()
            writer.writerows(list_of_dicts)

    return primaries


def make_3(leksiko, entity, primars):
    if entity=='Writer':

        informs = ['Αύριο στις 11 \n      γενική συνάντηση', 'Πάρε άμεσα το αφεντικό',
                   'Η παρουσίαση θα γίνει \n         την Παρασκευή', 'Ένας συγγραφέας θα \n       περάσει το απόγευμα για συμβόλαιο']
        recommends = ['Ο καλύτερος εκδοτικός \n       οίκος της δεκαετίας', 'Αξεπέραστη \n       ποιότητα βιβλίων',
                      'Εξαιρετικά φιλικοί \n       με τους πελάτες', 'Επιλέγουν σοφά \n       τους συγγραφείς τους']
        genres = ['Φαντασίας', 'Επιστημονικής φαντασίας', 'Δυστοπικά', 'Δράσης και περιπέτειας', 'Μυστηρίου', 'Θρίλερ', 'Αστυνομικά', 'Ιστορικής φαντασίας',
                  'Ρομαντικά', 'Μικρού μήκους', 'Σύγχρονης φαντασίας', 'Φιλοσοφικά', 'Νουβέλες', 'Γραφικά',
                  'Εφηβικά', 'Νεανικά ', 'Παιδικά', 'Αυτοβιογραφίες', 'Θεολογικά', 'Τέχνης', 'Ιστορικά', 'Αληθινά εγκλήματα', 'Σατιρικά',
                  'Επιστημονικά', 'Κοινωνικών επιστημών', 'Ακαδημαϊκά', 'Τεχνολογίας', 'Ταξίδια και Φαγητό']
        education = ['Λύκειο', 'Πανεπιστήμιο', 'Μεταπτυχιακό', 'Διδακτορικό']
        dimensions = ['30 x 48', '17 x 23  ', '15 x 23 ', '10 x 17 ']
        action_details_supply = [
            'Αναμένεται καθυστέρηση λόγω \n       προβλημάτων στη εφοδιαστική αλυσίδα', 'Αναμένεται εντός του μήνα']
        action_details_print = [
            'Αναμένεται καθυστέρηση λόγω\n       βλάβης εκτυπωτή', 'Η εκτύπωση ξεκινά από αύριο']
        purchase_details = ['1ος όροφος', 'Λείπει τα Σ/Κ',
                            'Διαθέσιμος για παραλαβή \n        από Δευτέρα', 'Στείλτε όλη την \n       παρτίδα σε μια αποστολή']
        copyrights = ['All rights reserved',
                      'Some rights reserved', 'No rights reserved']
        action_type = ["Προμήθεια", "Εκτύπωση"]
        volumes = ['1x2x3', '1x1x1', '2x2x2', '0.2x0.2x0.1']
        percentage_on_sales = np.arange(start=0.1, stop=0.5, step=0.05)
        immediate_payments = [1000.0, 2000.0, 3000.0, 8000.0]
        book_weights = [0.2, 0.8, 1.5, 2.2]
        total_weights = [2, 10, 30, 1200]
        locs = ['senario1.txt', 'senarioxionaths.txt', 'senariostaxtopoutas.txt']
        avails = [200, 40, 400, 1800]
        pages = [20, 50, 600, 1050]
        quantities = [20, 50, 200, 800]
        count = [8, 80, 800, 1800]
        pr_levels = [1, 2, 3, 4]
        targeted_audieces = ['Παιδιά', 'Έφηβοι',
                             'Φοιτητές', 'Ενήλικες', 'Γονείς', 'Γυναίκες', 'Άντρες']
        primaryKey = 1
        entity_diction = leksiko[entity]
        list_of_dicts = []
        primaries = []
        end = 19 #together with printing facilities must be les than partners (this is Writer)
        for i in range(1, end):
            temp_dict = {}
            for attribute in entity_diction.keys():
                typos = entity_diction[attribute][0]
                primary = entity_diction[attribute][1]
                name = attribute
                if len(entity_diction[attribute]) < 4:
                    if primary == False:
                        if typos == 'integer':
                            if name == 'Avail':
                                temp_dict[name] = avails[random.randint(0, 3)]
                            elif name == 'Pages':
                                temp_dict[name] = pages[random.randint(0, 3)]
                            elif name == 'Quantity':
                                temp_dict[name] = quantities[random.randint(0, 3)]
                            elif name == 'Count':
                                temp_dict[name] = count[random.randint(0, 3)]
                            elif name == 'Pr_level':
                                temp_dict[name] = pr_levels[random.randint(0, 3)]
                        elif typos == 'text':
                            if name == 'Genre' and i < len(genres):
                                temp_dict[name] = genres[i]
                            elif name == 'Targeted_Audience':
                                temp_dict[name] = targeted_audieces[random.randint(
                                    0, 6)]
                            elif name == 'Information' and entity == 'Informs':
                                temp_dict[name] = informs[random.randint(0, 3)]
                            elif name == 'Information' and entity == 'Recommendation':
                                temp_dict[name] = recommends[random.randint(0, 3)]
                            elif name == 'Education':
                                temp_dict[name] = education[random.randint(0, 3)]
                            elif name == 'Copyrights':
                                temp_dict[name] = copyrights[random.randint(0, 2)]
                            elif name == 'Dimensions':
                                temp_dict[name] = dimensions[random.randint(0, 3)]
                            elif name == 'ISBN':
                                temp_dict[name] = fake.unique.isbn10()
                            elif name == 'Action_type':
                                act_type = action_type[random.randint(0, 1)]
                                temp_dict[name] = act_type
                            elif name == 'Details' and entity == 'Production_Action':
                                if act_type == 'Προμήθεια':
                                    temp_dict[name] = action_details_supply[random.randint(
                                        0, 1)]
                                elif act_type == 'Εκτύπωση':
                                    temp_dict[name] = action_details_print[random.randint(
                                        0, 1)]
                            elif name == 'Details' and entity == 'Purchase':
                                temp_dict[name] = purchase_details[random.randint(
                                    0, 3)]
                            elif name == 'Total_volume':
                                temp_dict[name] = volumes[random.randint(0, 1)]
                            else:
                                temp_dict[name] = get_random_string(
                                    random.randint(1, 64))
                        elif typos == 'float':
                            if name == 'Percentage_on_sales':
                                temp_dict[name] = round(percentage_on_sales[random.randint(
                                    0, 7)], 2)
                            elif name == 'Immidiate_payment':
                                temp_dict[name] = immediate_payments[random.randint(
                                    0, 3)]
                            elif name == 'Book_weight':
                                temp_dict[name] = round(book_weights[random.randint(
                                    0, 3)], 2)
                            elif name == 'Cost':
                                temp_dict[name] = round(
                                    random.uniform(10.00, 2000.00), 2)
                            elif name == 'Total_weight':
                                temp_dict[name] = round(total_weights[random.randint(
                                    0, 3)], 2)
                            else:
                                temp_dict[name] = round(1/random.randint(1, 15), 2)

                        elif typos == 'date':
                            temp_dict[name] = fake.date()

                        elif typos == 'binary':
                            temp_dict[name] = "\n" + \
                                str(path+locs[random.randint(0, 2)])

                    else:
                        while True:
                            temp = primaryKey
                            primaryKey += 1
                            if temp not in primaries:
                                temp_dict[name] = temp
                                primaries.append(temp)
                                break
                elif len(entity_diction[attribute]) == 4:
                    if primary == True:
                        while True:
                            temp = random.choice(get_relevant(
                                entity_diction[attribute][2], entity_diction[attribute][3]))
                            if temp not in primaries:
                                temp_dict[name] = temp
                                primaries.append(temp)
                                break
                    else:
                        temp_dict[name] = random.choice(get_relevant(
                            entity_diction[attribute][2], entity_diction[attribute][3]))

            list_of_dicts.append(temp_dict)
            with open('{}.csv'.format(entity), 'w', encoding='utf8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=entity_diction.keys())
                writer.writeheader()
                writer.writerows(list_of_dicts)

        return primaries
        








        

    facility_types = ['Μικρής κλίμακας',
                      'Μεσαίας κλίμακας', 'Μεγάλης κλίμακας']
    capabilities = ['Ενσωματωμένος \n     σελιδοδείκτης',
                    'Εξώφυλο με υφή', 'QR code', 'Κανονικές', 'Κανονικές', 'Κανονικές', 'Κανονικές', 'Κανονικές', 'Κανονικές']
    primaryKey = 1
    entity_diction = leksiko[entity]
    list_of_dicts = []
    primaries = primars['Writer']
    end = 5 #together with writers must be les than partners (this is printing facility)
    for i in range(1, end):
        temp_dict = {}
        for attribute in entity_diction.keys():
            typos = entity_diction[attribute][0]
            primary = entity_diction[attribute][1]
            name = attribute
            if len(entity_diction[attribute]) < 4:
                if primary == False:
                    if typos == 'text':
                        if name == 'Facility_type':
                            temp_dict[name] = facility_types[random.randint(
                                0, 2)]
                        elif name == 'Capabilities':
                            temp_dict[name] = capabilities[random.randint(
                                0, 8)]
                if primary == True:
                    while True:
                        temp = primaryKey
                        primaryKey += 1
                        if temp not in primaries:
                            temp_dict[name] = temp
                            primaries.append(temp)
                            break
            elif len(entity_diction[attribute]) == 4:
                while True:
                    temp = random.choice(get_relevant(
                        entity_diction[attribute][2], entity_diction[attribute][3]))
                    if temp not in primaries:
                        temp_dict[name] = temp
                        primaries.append(temp)
                        break

        list_of_dicts.append(temp_dict)
        with open('{}.csv'.format(entity), 'w', encoding='utf8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=entity_diction.keys())
            writer.writeheader()
            writer.writerows(list_of_dicts)

    return primaries


prims = {}
client_prim = make_1(entities_properties, 'Client')
employee_prim = make_1(entities_properties, 'Employee')
partner_prim = make_1(entities_properties, 'Partner')
prims['Client'] = client_prim
prims['Employee'] = employee_prim
prims['Partner'] = partner_prim
prims['Informs'] = make_2(entities_properties, 'Informs', prims)
prims['Recommendation'] = make_2(entities_properties, 'Recommendation', prims)
prims['Category'] = make_2(entities_properties, 'Category', prims)
prims['Writer'] = make_3(entities_properties, 'Writer', prims)
prims['Printing_Facility'] = make_3(
    entities_properties, 'Printing_Facility', prims)
prims['Contract'] = make_2(entities_properties, 'Contract', prims)
prims['Book'] = make_2(entities_properties, 'Book', prims)
prims['Batch'] = make_2(entities_properties, 'Batch', prims)
prims['Production_Action'] = make_2(
    entities_properties, 'Production_Action', prims)
prims['Purchase'] = make_2(entities_properties, 'Purchase', prims)
