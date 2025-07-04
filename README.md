<!-- trunk-ignore-all(markdownlint/MD026) -->

# 🔐 CHATLEX – Secure. Anonymous. Decentralized.

A next-generation messenger designed with uncompromising focus on privacy,
security, and anonymity.

> 🚧 Active Development – Regular updates underway. Check the
> [Roadmap](#-roadmap)
> for what’s coming next.
>
> 🤝 Open Source & Community Driven
> Contributions are welcome! If you have ideas, issues, or improvements,
> feel free to open an issue, submit a pull request or join my
> [Dev-Club](https://discord.gg/kDwsjn9U8F) to contribute!
<!-- trunk-ignore(markdownlint/MD028) -->

> ## ⚠️ Legal Disclaimer
>
> **CHATLEX** is created for lawful, educational, and research purposes only.
> Misuse is strictly discouraged.
> By using this software, you accept full responsibility for ensuring
> your compliance with local
> laws and regulations regarding encryption and communication.
>
> - We do NOT support or assist with illegal activities.
> - Use of this software is entirely at your own risk.
> - The developers and contributors assume no liability for any
> misuse or consequences arising from use.

## 🔒 Our Security & Privacy Principles

- No central servers – Peer-to-peer architecture only.
- Zero data collection – We collect nothing from users.
- No backdoors. **Ever**.
- Fully open-source under AGPLv3.
- End-to-end encrypted using modern cryptographic standards.

## 💡 Suggest Enhancements

You have any suggestions on how to enhance its safety and anonymity?
Feel free to open an issue or start a discussion in the GitHub Repository.

## ✨ Core Features

| Features                | Description                                                                                                            | Implemented |
| ----------------------- | ---------------------------------------------------------------------------------------------------------------------- | ----------- |
| Decentralized Messenger | No server between your messages                                                                                        | ✅          |
| Password Generation     | A key will be derived with salt and pepper to make the entered password unique                                         | ✅          |
| Data                    | Your data will be stored **locally only**, encrypted                                                                   | ✅          |
| Platforms               | Android                                                                                                                | ✅          |
| Open Source             | Transparent codebase for public scrutiny and trust                                                                     | ✅          |
| Key Derivation          | The code uses Argon2 to derive the master key and AES-CBC to derive a new key for each message to encrypt the messages | ✅          |
| Encryption              | AES_256_GCM-265, ECDHE, Kyber                                                                                              |             |
| Data Transmission       | The data will be sent over the Tor network to anonymize the traffic                                                    |             |
| Group Chats             | Group chats for chatting with multiple people - just like WhatsApp or Signal                                           |             |
| File Sharing            | Sharing files up to 500 MB                                                                                             |             |

## 📈 Roadmap

- ✅ Storage logic (encryption, database)
- 🚧 Pages and appearance management
- Adding Contacts
- Sending (P2P)
- Group Chats
- Multi Device Sync
- File Sharing (image, video, audio, ...)

## 🛠 Current Tech Stack Highlights

- **Language:** Python
- **Encryption:** AES-256-CBC
- **Hashing:** Argon2, HKDF
- **Storage:** Encrypted SQLite3

## 🧾 Fonts

The fonts used in this project are sourced from [Google Fonts](https://fonts.google.com/).

**Currently supported:**

- Baloo Bhaijaan
- Baloo Bhaijaan semibold _(default)_
- Dosis semibold
- Varela Round

## 💬 Community & Support

Have questions, concerns, or suggestions?
Open an issue or contribute directly via GitHub.
