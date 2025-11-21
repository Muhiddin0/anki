import requests


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



for note in notes[0:1]:
  
    note_id = note["noteId"]

    # mavjud fields
    updated_fields = {fname: fdata["value"] for fname, fdata in note["fields"].items()}
    word = note['fields']["Word"]
    meaning = note['fields']["Meaning"]
    example = note['fields']["Example"]

    # yangi field qo'shish
    updated_fields["Tarjima"] = "Bu yangi maydon qiymati"
    updated_fields["Manosi"] = "Bu yangi maydon qiymati"
    updated_fields["Misol"] = "Bu yangi maydon qiymati"
    
    # note fieldlarini update qilish
    response = anki("updateNoteFields", {
        "note": {
            "id": note_id,
            "fields": updated_fields
        }
    })

    # print(response.status_code)
    print(response)


#     note_id = note["noteId"]
#     fields = note["fields"]

#     # Har bir note kamida 1 ta cardga ega
#     card_id = note["cards"][0]

#     # 3) Card info orqali deck nomini olish
#     card_info = anki("cardsInfo", {"cards": [card_id]})[0]
#     deck_name = card_info["deckName"]

#     print(note)
