# ZEPHRA

A messenger, designed with a strong focus on security and anonymity.

> 🚧 **Project in Progress!** – Regular updates are being made. View [Roadmap](#roadmap) for more info

> **Contributions Welcome!**
>
> This is an open-source project. If you'd like to help improve the messenger,
> feel free to fork the repository, suggest enhancements, or report issues.

> ## ❗NOTE
>
> **ZEPHRA is intended for lawful use only. The developers do not condone illegal activity.**

> ## ❗Legal Disclaimer
>
> This project is provided for **educational and research purposes only**. The developers and contributors are **not responsible** for how this software is used.
>
> Use of this software is at your own risk. You are solely responsible for complying with local laws and regulations regarding privacy, encryption, and communication.
>
> We explicitly **do not condone illegal activity** and will not provide support for misuse of this project.
>
> ## Important Notes
>
> - We do not collect or store any data.
> - We will not implement backdoors.
> - This project is fully open-source under the AGPLv3 license.

## Your ideas

If you have any suggestions on how to enhance its safety and anonymity,
feel free to open an issue in the GitHub repository.

## Features

| Features                | Description                                                                                                            | Implemented |
| ----------------------- | ---------------------------------------------------------------------------------------------------------------------- | ----------- |
| Decentralized Messenger | No server between your messages                                                                                        | ✅          |
| Encryption              | AES-265, ECDHE, Kyber                                                                                                  |             |
| Password Generation     | A key will be derived with salt and pepper to make the entered password unique                                         | ✅          |
| Data                    | Your data will be stored **locally only**, encrypted                                                                   | ✅          |
| Platforms               | Android                                                                                                                | ✅          |
| Data Transmission       | The data will be sent over the Tor network to anonymize the traffic                                                    |             |
| Open Source             | Transparent codebase for public scrutiny and trust                                                                     | ✅          |
| Key Derivation          | The code uses Argon2 to derive the master key and AES-CBC to derive a new key for each message to encrypt the messages | ✅          |
| Group Chats             | Group chats for chatting with multiple people - just like WhatsApp or Signal                                           |             |
| File Sharing            | Sharing files up to 500 MB                                                                                             |             |
| Image Sharing           | Sharing high quality images                                                                                            |             |

📌 **Notice!** The project is still in progress-some features may not be included yet.

## Roadmap

- 🚧 Basic implementations like encrypting and sending (P2P)
- Adding Contacts
- Group Chats
- File Sharing
- Image Sharing
- Video Sharing

## Fonts

The fonts used in this project are sourced from [Google Fonts](https://fonts.google.com/).

**Currently supported:**

- Baloo Bhaijaan
- Varela Round
