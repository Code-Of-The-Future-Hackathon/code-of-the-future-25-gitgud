# HomePet 🏠🐾

HomePet is a **smart pet management system** built with Django, allowing pet owners to effortlessly monitor and control every aspect of their furry friend's wellbeing—**feeding**, **watering**, **door access**, and **location tracking**.

---
## Table of Contents
1. [Features](#features)
2. [Technologies](#technologies)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Screenshots](#screenshots)
6. [Contributing](#contributing)
7. [License](#license)
8. [Contact](#contact)

---

## Features

### 🎛️ Dynamic, Widget-Based Dashboard
- **Drag & Drop Widgets:** Customize your layout by simply dragging and dropping widgets (Food, Water, Door, Location) wherever you like.
- **Real-Time Updates:** Changes to settings or data are reflected in real time through AJAX requests.

### 🍽️💧 Food & Water Management
- **Modes:**
    - **Manual** – Trigger feedings/waterings on-demand with a single click.
    - **Automatic** – Schedule feed/water times using either *timed* or *interval* modes.
- **Quantity Settings:** Easily set the amount of food (grams) and water (ml) for each feeding/watering.
- **Instant Actions:** If in Manual mode, click "Feed" or "Water" to supply your pet immediately.

### 🚪 Door Management
- **Modes:**
    - **Manual** – Open or close the pet door instantly with a single action.
    - **Automatic** – Set it to "Always Open" or schedule open/close times (24-hour format). Optionally, allow your pet to come back in after the door closes.
- **Logging:** Every manual action automatically creates a **DoorLog**, so you can keep track of openings/closings.

### 🗺️ Location Tracking
- **Custom Map Overlay:** Display your home’s floor plan (or any custom image) as the map background using Leaflet.js.
- **Real-Time Positioning:** Shows your pet’s **last known location**, centering the map on their most recent log.
- **Detailed Logs:** View timestamped **LocationLog** entries with descriptions and exact coordinates.

### 🤳 Responsive & Modern UI
- Built with **Bulma CSS**, **Font Awesome**, **jQuery**, and **jQuery UI** for a clean, mobile-friendly experience.
- Custom **Samsung Sans** font and **CSS variables** for a unique, modern aesthetic.

### ⚡ Smooth Interactivity
- **AJAX** & **jQuery** integration for quick saves, instant feedback, and seamless widget rearrangement.
- **Drag-and-Drop** functionality powered by **jQuery UI**—get your dashboard layout just the way you like it!

---

## Technologies
- **Backend:** Django (Python)
- **Frontend:** Bulma CSS, Font Awesome, jQuery, jQuery UI
- **Mapping:** Leaflet.js (with custom image overlay)
- **Styling:** Custom CSS using variables and the Samsung Sans font

---

## Installation
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Code-Of-The-Future-Hackathon/code-of-the-future-25-gitgud
   cd homepet
   ```
2. **Create & Activate a Virtual Environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure Your Database:**
    - Update `settings.py` with your database credentials and preferences.

5. **Run Migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Create a Superuser (optional):**
   ```bash
   python manage.py createsuperuser
   ```
7. **Collect Static Files:**
   ```bash
   python manage.py collectstatic
   ```
8. **Run the Development Server:**
   ```bash
   python manage.py runserver
   ```
    - Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

---

## Usage
1. **Login & Dashboard:**
    - Access the **HomePet** dashboard to see widgets for food, water, door status, and location in a **drag-and-drop** interface.

2. **Food & Water Settings:**
    - **Manual vs. Automatic** modes.
    - *Automatic* can be configured by time or interval.
    - Adjust **feed/water quantity** in grams/ml.
    - Click "**Feed**" or "**Water**" for instant actions in Manual mode.

3. **Door Management:**
    - **Manual** mode: Use quick-action buttons to open or close the pet door immediately.
    - **Automatic** mode:
        - **Always Open** or scheduled open/close times (e.g., open at 07:00, close at 21:00).
        - Optionally allow re-entry after close.
    - All manual actions create **DoorLog** records.

4. **Location Tracking:**
    - Check your pet’s **last known location** on the map (with a custom floor plan overlay).
    - Get detailed info like the timestamp and description of the latest **LocationLog**.

---

## License
This project is licensed under the [MIT License](LICENSE).

---

## Contact
**Questions or suggestions?**  
Reach out at [homepet@deyannikolov.eu](mailto:homepet@deyannikolov.eu)

---

Enjoy **HomePet**—your smart, modern solution for all your pet care needs! 🏠🐾  