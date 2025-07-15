#  Reddit User Persona Generator

Scrape any Reddit profile and generate a detailed, AI-powered **User Persona**—with citations. No Reddit API. No guesswork. Just real data, turned into actionable insights.

---

##  Why Use This?

Ideal for:
- UX & Product Research  
- Behavioral Targeting  
- Persona-Driven Design  
- Marketing, Branding & Copy Strategy

This tool reverse-engineers Reddit users into richly detailed personas using real digital footprints.

---

## Features

Scrapes latest **posts & comments** from any public Reddit profile  
Uses **Claude 3 Haiku via OpenRouter** to analyze and synthesize traits  
Outputs a structured **persona profile** in `.txt` and `.json`  
Includes **citations** from actual Reddit activity  
Optional Flask UI with styled persona web page  
**No Reddit API required** (pure scraping)

---

##  Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/tejaswigadhe/Reddit-Persona-Generator
cd Reddit-Persona-Generator
```

### 2. Create Virtual Environment

```bash
python -m venv venv
# Activate it:
venv\Scripts\activate     # Windows
source venv/bin/activate  # macOS/Linux
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Add OpenRouter API Key

Create a `.env` file:

```env
OPENROUTER_API_KEY=your_api_key_here
```

---

## How to Run

```bash
python reddit_persona.py
```

Paste any Reddit profile URL when prompted:

```
https://www.reddit.com/user/kojied/
```


## 🌐 Optional Flask Web UI

To run the web interface:

```bash
python app.py
```

Open [http://localhost:5000](http://localhost:5000)  
Upload a Reddit URL and view the styled persona page.

---

## Repo Structure

```
reddit-user-persona/
├── app.py                    # Flask app (optional UI)
├── reddit_persona.py         # Core scraping + persona logic
├── requirements.txt
├── .env                      # API key (not tracked)
├── static/
│   └── persona.css           # Web styling
├── templates/
│   ├── index.html
│   ├── error.html
│   ├── persona.html
│   └── populate.js
├── output/
│   └── persona.json
└── README.md
```

---

##  Sample Output Includes:

- **Name, Age, Occupation, Status, Location**
- **Personality Type (MBTI), Motivations, Behaviors**
- **Goals, Frustrations, Quotes**
- **Archetype Classification**
- **Cited Evidence from Reddit Comments**

---

## Ethical Note

This tool **does not use Reddit’s API**. It scrapes only publicly available data and is intended strictly for ethical use, research, and innovation.

---

## License

MIT License

```
MIT License

Copyright (c) 2025 

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights   
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell      
copies of the Software, and to permit persons to whom the Software is          
furnished to do so, subject to the following conditions:                        

The above copyright notice and this permission notice shall be included in     
all copies or substantial portions of the Software.                            

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR     
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,       
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE    
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER         
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,  
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN      
THE SOFTWARE.
```

---

## Innovation Outlook

> Personas shouldn’t be static PDF files.  
> They should evolve with your users.  
> Let’s build tools that reflect that.

---
