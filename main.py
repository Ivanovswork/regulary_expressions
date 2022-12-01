import csv
import re


def forming_of_list(contacts_list):
    pattern = r"(\w+)[, -]*(\w+)[, -]*([^, -]*)[, -]*(\w*)[, -]*([^,]*)[,]*([^,]*)[, -]*(.*)"
    contacts = []
    for row in contacts_list:
      c = [x for x in re.split(pattern, row[0]) if x != ""]
      contacts.append(c)
    contacts.pop(0)

    for i in range(0, len(contacts)):
      for j in range(i + 1, len(contacts)):
        if contacts[i][0] == contacts[j][0] and contacts[i][1] == contacts[j][1]:
          contacts[i].extend(contacts[j])
          contacts[j][0], contacts[j][1] = i, j

    for elem in contacts:
      if type(elem[0]) == int and type(elem[1]) == int:
        contacts.remove(elem)

    return contacts


def end_of_forming(contacts):
    right_contacts = []
    for e in contacts:
        pat = [' нет информации' for i in range(7)]
        number_of_name = 0
        count_of_postion = 0
        for elem in e:
            # print([elem])
            # print(re.findall(r"(\w+)", elem))
            if re.findall(r"(\w+)", elem) == [elem] and elem != "Минфин" and elem != "ФНС" and number_of_name < 3:
                pat[number_of_name] = elem
                number_of_name += 1
            elif elem == "Минфин" or elem == "ФНС":
                pat[3] = elem
            elif re.findall(r"([^@.0-9+]+)", elem) == [elem] and len(re.findall(r"(\w+)", elem)) > 1 and count_of_postion == 0:
                pat[4] = elem
                count_of_postion += 1
            elif re.findall(r"([^,@А-ЯЁ]*)", elem) == [elem, ""]:
                sp = "".join(re.findall(r"\d", elem))
                if len(sp) == 11:
                    pattern = r"(\d{1})(\d{3})(\d{3})(\d{2})(\d{2})"
                    sp = re.sub(pattern, r"+7(\2)\3-\4-\5", sp)
                else:
                    pattern = r"(\d{1})(\d{3})(\d{3})(\d{2})(\d{2})(\d{4})"
                    sp = re.sub(pattern, r"+7(\2)\3-\4-\5 доб.\6", sp)
                pat[5] = sp
            elif "@" in elem and "." in elem:
                pat[6] = elem
        right_contacts.append(pat)

    return right_contacts


if __name__ == '__main__':
    with open("phonebook_raw.csv", encoding='utf-8') as f:
        rows = csv.reader(f, delimiter="\n")
        contacts_list = list(rows)
    with open("phonebook.csv", "w") as f:
          datawriter = csv.writer(f, delimiter=',')
          datawriter.writerows(end_of_forming(forming_of_list(contacts_list)))