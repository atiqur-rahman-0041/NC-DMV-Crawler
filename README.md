# NC DMV Appointment Crawler

Sick of spending your time waiting in the DMV walk-in line? Can’t snag an appointment even when you hit “refresh” a hundred times? Meet your new best friend—this little script will do the heavy lifting for you. It continuously polls the North Carolina DMV site for your chosen office and pings your Discord when a slot opens up (within the next 30 days by default).

> **Warning:** I’m not the DMV. No guarantees. But hey, it worked for me—so maybe there’s hope for you, too. If you really can’t be bothered to set it up yourself, feel free to bribe me with lunch and I’ll host it … until my stomach says otherwise.

---

## 🎉 Features

- **Discord pings** when an appointment slot pops up (no carrier pigeons needed)  
- **Dockerized**—one `docker compose up`, zero dependency headaches  
- **Loop forever** (or until you get bored)—checks every minute by default  
- **Configurable**: adjust location, appointment type, date range, and poll interval  

---

## 🛠️ Prerequisites

- Docker & Docker Compose (because who wants to fight with Python versions?)  
- (Optional) Python 3.11+ if you’d rather run it natively
- Make (because automating boring stuff is the best kind of laziness)  
- A Discord webhook URL (see [Intro to Webhooks](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks))  

---

## ⚙️ Configuration

- `NC_DMV_LOCATION`: The name of the NC DMV location to check (e.g. `Raleigh West`)
- `DISCORD_WEBHOOK_URL`: The URL of the Discord webhook to send notifications to
- `LOWER_DAY_RANGE`: The number of days before the current date to start checking for appointments (default: 0)
- `UPPER_DAY_RANGE`: The number of days after the current date to stop checking for appointments (default: 30)
- `APPOINTMENT_TYPE`: The type of appointment to check for (e.g. `Driver License - First Time`)
- `SELENIUM_URL`: Change this if you know what you're doing
- `POLL_INTERVAL`: The number of seconds to wait between checks (default: 60). To change this, you'll need to edit the Dockerfile. You can find it at the bottom of the file.

---

## 🚀 Installation & Usage

- Clone the repository
- Set up your `.env` file
- cd into the directory and run `make up`
- Make sure to keep your device open and connected to the internet
- You should start receiving notifications in your Discord channel if there are any appointments available
- If no appointment is available, you will see a log like "❌ Timeout while waiting for an element". This is not an error in setup or anything. I added this log for a sanity check, You can comment it out or change it if it bothers you too much.
- If you want to stop the crawler, you can run `make down`

---

## 🤝 Acknowledgments

Made possible by caffeine, stubbornness, and a little help from AI.

Totally not endorsed by NC DMV. No warranties, no refunds, no DMV employees were harmed in the making.

Enjoy your newfound free time—and good luck at the DMV! 🚗🎉
