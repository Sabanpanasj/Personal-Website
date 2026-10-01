# Portfolio resume website (Python + Netlify)

Dark theme, amber accents, a photo behind your name, and a floating bottom menu (Home, About, Projects, Skills, Contact).

## 1. Add your details
- Open `resume_data.py` and replace the placeholder text (name, email, phone, school, skills, projects, social usernames).
- Your photo is in `assets/profile.jpg`. To use a different photo, replace that file (or change `PHOTO` in `resume_data.py`). A PNG with a transparent background also works well. With no photo you get a soft blue glow.
- Put your resume in `assets/resume.pdf` to show the "Download Resume" button.
- Project pictures (optional): save them in `assets/` and set `"image": "assets/project1.png"` in `resume_data.py`.

## 2. Test on your computer
```
python serve.py
```
Your browser opens at http://localhost:8000. Refresh the page after editing `resume_data.py` and the changes show up right away. Press Ctrl+C in the terminal to stop.

The contact form shows the "Message sent" page and prints the message in the terminal, but it does not send a real email. Real emails start working after you deploy on Netlify.

To use another port: `python serve.py 3000`

### Test on your phone or tablet
1. Connect the phone to the same Wi-Fi as your computer.
2. Run `python serve.py` and look for the line "On your phone (same Wi-Fi): http://...".
3. Type that address into the phone's browser.

To keep the test private to your computer only, run `python serve.py --local-only`.

The site adjusts to phones, tablets, laptops and large screens. On small screens the menu shows icons only, and the active section shows its name.

## 3. Deploy on Netlify
1. Upload this folder to a GitHub repository.
2. In Netlify: Add new site > Import an existing project > choose the repository.
3. Netlify reads `netlify.toml` (build command `python build.py`, publish folder `dist`). Click Deploy.

## 4. Get messages in your email
1. Netlify > your site > Forms. After the first deploy you will see a form called `contact`.
2. Site configuration > Notifications > Form submission notifications > Add notification > Email notification.
3. Enter your personal email, choose the `contact` form, and save. Then send yourself a test message.

## Facebook, Instagram and TikTok
Websites cannot send messages into these apps automatically, so the round icons link to them:
- Facebook opens a Messenger chat with you
- Instagram opens a DM to you
- TikTok opens your profile
