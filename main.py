import requests
from colorama import just_fix_windows_console
from datetime import datetime
from termcolor import colored

just_fix_windows_console()

print(colored("Welcome to anime_pix v0.1", "white", "on_blue"))
print(colored("(c) 2024 XnonXte", "white", "on_blue"))


def get_waifu(is_nsfw, tag, many):
    url = (
        f"https://api.waifu.im/search?included_tags={tag}&many={many}&is_nsfw={is_nsfw}"
    )
    response = requests.get(url)

    if response.ok:
        return response.json()
    else:
        raise Exception(f"{response.status_code} - {response.reason}")


def download_image(url, path):
    data = requests.get(url).content
    with open(path, "wb") as file:
        file.write(data)


while True:
    versatile_tags = [
        "maid",
        "waifu",
        "marin-kitagawa",
        "mori-calliope",
        "raiden-shogun",
        "oppai",
        "selfies",
        "uniform",
    ]
    nsfw_tags = ["ass", "hentai", "milf", "oral", "paizuri", "ecchi", "ero"]

    is_nsfw = input(colored("NSFW (y/n): ", "magenta")).lower() == "y"
    nsfw_prompt_message = (
        colored("Yes NSFW >=)", "yellow")
        if is_nsfw
        else colored("No NSFW :)", "yellow")
    )
    print(nsfw_prompt_message)
    is_many = input(colored("Multiple results (y/n): ", "magenta")).lower() == "y"
    many_prompt_message = (
        colored("An upward of 30 results would be retrieved.", "yellow")
        if is_many
        else colored("Only 1 result would be retrieved.", "yellow")
    )
    print(many_prompt_message)
    availability_message = (
        colored(f"Available NSFW tags: {', '.join(nsfw_tags)}", "green")
        if is_nsfw
        else colored(f"Available versatile tags: {', '.join(versatile_tags)}", "green")
    )
    warning_message = colored(
        f"Not a valid {'NSFW' if is_nsfw else 'versatile'} tag! Please try again.",
        "white",
        "on_red",
    )
    selected_tags = nsfw_tags if is_nsfw else versatile_tags

    print(availability_message)
    tag = input(colored("Tag: ", "magenta"))

    if tag.lower() not in selected_tags:
        print(warning_message)
        continue

    print(colored(f"Chosen tag: {tag}", "yellow"))
    images = get_waifu(is_nsfw, tag, is_many)["images"]

    for count, image in enumerate(images, start=1):
        try:
            date_now = int(datetime.now().timestamp())
            url = image["url"]
            ext = image["extension"]
            file_name = f"anime_pix-{tag}-{date_now}{ext}"
            file_path = f"./downloads/{file_name}"

            download_image(url, file_path)
            print(colored(f"Image {count} out of {len(images)} downloaded!", "green"))
        except Exception as e:
            print(
                colored(
                    f"Image {count} out of {len(images)} couldn't get downloaded! Error: {e}",
                    "white",
                    "on_red",
                ),
            )

    is_continue = (
        input(colored("Do you want to continue (y/n): ", "magenta")).lower() == "y"
    )
    if not is_continue:
        print(colored("Thanks for using my program!", "white", "on_blue"))
        break
