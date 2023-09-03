import argparse
import requests

BASE_URI = 'http://localhost:5000/movie'


def note_to_json(name, content):
    return {
        "name": name,
        "content": content,
    }


def add_note(name, content):
    json_note = note_to_json(name, content)
    headers = {'Content-Type': 'application/json'}
    requests.post(BASE_URI, json=json_note, headers=headers)


def delete_note(id):
    requests.delete(f'{BASE_URI}/{id}')


def modify_note(name, content, id):
    json_note = note_to_json(name, content)
    headers = {'Content-Type': 'application/json'}
    requests.put(f'{BASE_URI}/{id}', json=json_note, headers=headers)


def display_note(id):
    if id is None:
        response = requests.get(f'{BASE_URI}')
    else:
        response = requests.get(f'{BASE_URI}/{id}')
    print(response.text)


def main():
    parser = argparse.ArgumentParser(description="Note Manager")
    parser.add_argument("note", choices=["add", "delete", "display", "edit"],
                        help="actions to perform")
    parser.add_argument("--note_id", type=int,
                        help="Note ID (for delete and edit actions)")
    parser.add_argument("--name",
                        help="Note title (for add and edit actions)")
    parser.add_argument("--content",
                        help="Note content (for add and edit actions)")
    args = parser.parse_args()

    if args.note == "add":
        add_note(args.name, args.content)
    elif args.note == "delete":
        delete_note(args.note_id)
    elif args.note == "edit":
        modify_note(args.name, args.content, args.note_id)
    elif args.note == "display":
        display_note(args.note_id)


if __name__ == "__main__":
    main()
