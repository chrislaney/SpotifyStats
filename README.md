# SpotifyStats
# UNREVISED_WIP Final Fall Design Report UNREVISED_WIP

# Final Fall Design Report

## Table of Contents
1. [Team and Project](#team-and-project)
2. [Project Description](#project-description)
3. [User Stories and Design Diagrams](#user-stories-and-design-diagrams)
   - [User Stories](#user-stories)
   - [Design Diagrams](#design-diagrams)
4. [Project Tasks and Timeline](#project-tasks-and-timeline)
   - [Task List](#task-list)
   - [Timeline](#timeline)
   - [Effort Matrix](#effort-matrix)
5. [ABET Concerns Essay](#abet-concerns-essay)
6. [PPT Slideshow](#ppt-slideshow)
7. [Self-Assessment Essays](#self-assessment-essays)
8. [Professional Biographies](#professional-biographies)
9. [Budget](#budget)
10. [Appendix](#appendix)

---

## Team and Project
**Team Members:**  

**William Hawkins** - Faculty Advisor   
Email: [hawkinwh@ucmail.uc.edu](mailto:hawkinwh@ucmail.uc.edu)

---

**Seamus Collins** - Computer Science Student   
Email: [colli2sc@mail.uc.edu](mailto:colli2sc@mail.uc.edu)

**Noah Falanga** - Computer Science Student   
Email: [falangnm@mail.uc.edu](mailto:falangnm@mail.uc.edu)

**Chris Laney** - Computer Science Student   
Email: [Laneyct@mail.uc.edu](mailto:Laneyct@mail.uc.edu)

**Justin Tisch** - Computer Science Student   
Email: [tischjl@mail.uc.edu](mailto:tischjl@mail.uc.edu)

---



**Project Abstract:**  
#### REVISE ME?
We are building a webapp that uses the Spotify API to pull users data, and extrapolate information about their listening history either directly or indirectly from the data given. This will be parsed by a backend system and then distributed to the frontend and also another backend component will utilize learning techniques in order to provide new music recommendations for the user. In essence there will be two visible portions to the project; the historical analysis interface and future prediction interface, all brought together by a backend parser/controller.​

---

## Project Description
### REVISE ME 
Our topic area is a spotify analytics web app. There are two components to the project, a portion that breaks down current listening history and habits and a portion that uses listening history with other deduction strategies to reccomend music to the user. This will all be tied up in a very aesthetic UI/UX.

---

## User Stories and Design Diagrams

### User Stories

As an individual SpotifyStats user, I would like to get new music recommendations based on my current/past listening habits so that I can enjoy more new music.

As a SpotifyStats user, I would like the UI to be in the 80s retro style, because it's visually pleasing.

As a system, I would like to report errors from any third-party API calls, so that software developers can debug any user problems.

As a SpotifyStats developer I would like to be able to access Spotify data that is already cleaned with a straightforward method of retrieval so that it can be used in many parts of the application.


### Design Diagrams
#### Level 0 Diagram
![Level 0 Diagram](./revised/design_diagrams/level_0.png) 
[Level 0 Description](./revised/design_diagrams/level_0_desc.md)
#### Level 1 Diagram
![Level 1 Diagram](./revised/design_diagrams/level_1.png) 
[Level 1 Description](./revised/design_diagrams/level_1_desc.md)

#### Level 2 Diagram
![Level 2 Diagram](./revised/design_diagrams/level_1.png) 
[Level 2 Description](./revised/design_diagrams/level_1_desc.md)

---

## Project Tasks and Timeline

## Milestones
1. Retrieve the first Spotify data and display it on a webpage.
2. Complete data cleaning and storage processes alongside developing visual components and passing data to the algorithm backend.
3. Create an initial working version of a recommendation algorithm.
4. Implement dynamic data visualizations on the front end with live data.

--- 

### Task List 
1. Spotify  
   1. Research Spotify API
   2. Obtain a developer Spotify account 
   3. Integrate Spotify API into program 
      1. Connect to Spotify API
      2. Transform data into a Global Format I/O 
   4. Develop minimum viable product 
   5. Document use of Spotify API Integration 
   6. Develop data pipeline from backend to front 
2. Front End  
   1. Research \<CODE LANGUAGE\> front-end capabilities 
   2. Obtain sandbox environment 
   3. Design Proof of Concept page(s) 
   4. Develop minimum viable product 
   5. Document front-end navigation 
3. Recommendation Algorithm  
   1. Create Music History Analysis based on Global Format 
   2. Research Prediction Algorithm 
   3. Design Prediction Algorithm 
   4. Implement Prediction Algorithm using Global Format I/O
   5. Document each prediction algorithm and analysis profile



### Timeline
| **Task Description**                                            | **Start Date** | **End Date**   |
|------------------------------------------------------------------|----------------|----------------|
| Research Spotify API                                             | 10/1/24        | TBD            |
| Research framework/language for the web app                     | 10/1/24            | TBD            |
| Design proof-of-concept pages and mockups                       | 10/1/24            | TBD            |
| Create front-end navigation map                                  | TBD            | TBD            |
| Determine planned features accessible via frontend              | TBD            | 1/21/25        |
| Obtain sandbox environment                                       | 10/1/24            | 11/1/24        |
| Build out listening history section                              | TBD            | 4/12/25        |
| Build out recommendation section                                 | TBD            | 4/12/25        |
| Dynamic data pipeline from API to frontend                      | 1/1/25         | 4/20/25        |
| Host the website                                                 | TBD            | 4/1/25         |
| Minimum viable product (MVP) and presentation                   | 4/1/25         | 4/20/25        |
| Obtain Spotify developer account                                 | 10/14/24       | 10/21/24       |
| Connect to Spotify API                                           | 10/14/24       | 11/1/24        |
| Collect and clean data                                           | 10/14/24       | 1/1/25         |
| Parse and send data to frontend/recommendation algorithm         | 10/14/24       | 1/1/25         |
| Develop MVP and document Spotify API integration                | 4/1/25         | 4/20/25        |
| Create music history analysis based on retrievable Spotify data | 10/9/24        | 1/1/25         |
| Research prediction algorithms                                   | 10/9/24        | 3/1/25         |
| Design prediction algorithms                                     | 1/1/25         | 4/1/25         |
| Implement prediction algorithms and coordinate with frontend    | 1/1/25         | 4/1/25         |
| Document prediction algorithms                                   | 10/1/24        | 4/20/25        |
| Test and validate algorithms                                    | 3/1/25         | 4/20/25        |


### Effort Matrix
| **Task Description**                                   | **Assigned To**            | **Hours Estimated or Completed** |
|-------------------------------------------------------|----------------------------|-----------|
| Research Spotify API                                  | Seamus                     | 5         |
| Research framework/language for the web app           | Seamus                     | 4         |
| Design proof-of-concept pages and mockups             | All                        | 6         |
| Create front-end navigation map                       | Chris                      | 3         |
| Determine planned features accessible via frontend    | All                        | 3         |
| Obtain sandbox environment                            | Seamus, Chris              | 2         |
| Build out listening history section                   | Chris                      | 8         |
| Build out recommendation section                      | Chris                      | 8         |
| Dynamic data pipeline from API to frontend            | Seamus                     | 10        |
| Host the website                                      | Seamus                     | 5         |
| Minimum viable product and presentation               | All                        | 12        |
| Obtain Spotify developer account                      | All                        | 0.5       |
| Connect to Spotify API                                | Seamus                     | 1         |
| Collect and clean data                                | Noah                       | 8         |
| Parse and send data to frontend/recommendation algo   | Seamus                     | 6         |
| Create music history analysis                         | Noah,Justin                | 8         |
| Research prediction algorithms                        | Noah, Justin               | 6         |
| Design prediction algorithms                          | Noah, Justin               | 8         |
| Implement prediction algorithms and coordinate UI/UX  | Noah, Justin, Chris        | 15        |
| Pipeline data from backend to frontend                | Justin                     | 3         |
| Document prediction algorithms                        | Noah, Justin               | 4         |
| Test and validate algorithms                          | Noah                       | 12        |


---

## ABET Concerns Essay
**Summary:** 
SpotifyStats operates within several constraints, including security, ethics, economics, and legal compliance. 
Key considerations include safeily handling user data, adhering to Spotify and other API permissions, maintaining cost-effective development, and ensuring legal compliance. These constraints guide the design and implementation of our project, ensuring it remains secure, ethical, and accessible.

See the full [Constraint Essay](./ConstraintEssayRevised.pdf).

---

## PPT Slideshow
[PPT Slideshow](./SrDesignAssignment8.pptx.pptx)

[Video Presentation]([./].pptx]([https://mailuc-my.sharepoint.com/:v:/g/personal/yang2j7_mail_uc_edu/EVRr90AcgElMoHGHj1HDdtcB1DDXul0nM2fKfRxgdMAEvg?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJPbmVEcml2ZUZvckJ1c2luZXNzIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXciLCJyZWZlcnJhbFZpZXciOiJNeUZpbGVzTGlua0NvcHkifX0&e=aEcDCk)](https://mailuc-my.sharepoint.com/:v:/g/personal/laneyct_mail_uc_edu/EdBwQNEC7LdAmnYO8MOcC4gBi6mM51ssK-GU0cPHtDStDw?e=gQzECU&nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJTdHJlYW1XZWJBcHAiLCJyZWZlcnJhbFZpZXciOiJTaGFyZURpYWxvZy1MaW5rIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXcifX0%3D))

---

## Self-Assessment Essays
[Self-Assessment Essays Repo](./revised/essays) 

---

## Professional Biographies
[Self-Assessment Essays Repo](./revised/essays)  
Include brief biographies of team members.

---

## Budget
- **Expenses to Date:**  
  - NONE 
- **Monetary Value of Donations:**  
  - NONE

---

## Appendix
- **References:**  
  - [Spoitfy API WIKI](https://developer.spotify.com/documentation/web-api)
  
include appropriate references, citations, links to code repositories, and meeting notes.
there should be evidence justifying 45 hours of effort for each team member.

---
