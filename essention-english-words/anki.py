import requests
from translator import translate_word


def anki(action, params=None):
    r = requests.post(
        "http://127.0.0.1:8765",
        json={"action": action, "version": 6, "params": params or {}},
    ).json()

    if r["error"]:
        raise Exception("AnkiConnect xatosi: " + str(r["error"]))
    return r["result"]

deck_prefix = "4000 Essential English Words"
deck_numbers = range(1, 7)  # 1 dan 6 gacha
queries = [f'deck:"{deck_prefix}::{i}.Book"' for i in deck_numbers]
query = " or ".join(queries)

# query = 'deck:"4000 Essential English Words::test"'


# 1) Barcha note ID lar
note_ids = anki("findNotes", {"query": query})
print("Topilgan kartalar soni:", len(note_ids))

if not note_ids:
    print("Hech qanday karta topilmadi.")
    exit()

# 2) Note info
notes = anki("notesInfo", {"notes": note_ids})



for note in notes:
  
    note_id = note["noteId"]
    # mavjud fields
    updated_fields = {fname: fdata["value"] for fname, fdata in note["fields"].items()}
    word = note['fields']["Word"]['value']
    meaning = note['fields']["Meaning"]['value']
    example = note['fields']["Example"]['value']

    # yangi field qo'shish
    if not bool(note['fields']["Word"]['value']):
        updated_fields["Tarjima"] = translate_word(word, target_language='uz')
    if not bool(note['fields']["Manosi"]['value']):
        updated_fields["Manosi"] = translate_word(word=meaning, target_language='uz')
    if not bool(note['fields']["Misol"]['value']):
        updated_fields["Misol"] = translate_word(word=example, target_language='uz')

    # print(word)
    # print(updated_fields['Tarjima'])
    # print("---" * 30)

    # note fieldlarini update qilish
    response = anki("updateNoteFields", {
        "note": {
            "id": note_id,
            "fields": updated_fields
        }
    })
