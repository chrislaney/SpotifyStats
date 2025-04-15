# Music Taste Profile Analysis Project
## Meeting Notes and Development Timeline

*Each meeting was about an hour in length*

## Fall Semester 2024

### Meeting (09/01/2024) - Team Formation
- Team members finalized and agreed on project focus
- Project chosen: Music Taste Profile Analysis System using Spotify data
- Initial discussion of system architecture and technology stack

### Meeting (09/08/2024) - Team Member Bios and Self-Reflection
- Submitted team member bios with work experience summaries
- Individual self-reflective essays about curriculum and co-op experience
- Discussed preliminary system requirements and user stories

### Meeting (09/15/2024) - Faculty Advisor Confirmation
- Confirmed primary faculty advisor: Professor Hawkins
- Completed and submitted team contract with faculty approval
- Started initial exploration of Spotify API capabilities

### Meeting (09/22/2024) - High-Level System Design
- Submitted high-level system design
- Decided on Python Flask backend with DynamoDB database
- Selected scikit-learn for implementing machine learning clustering
- Defined core system components: data collection, analysis, and recommendation

### Meeting (09/29/2024) - Detailed System Design
- Submitted detailed system design including:
  - System architecture diagram
  - Authentication flow using Spotify OAuth
  - Data flow for user music taste analysis
- Defined clustering methodology for genre-based user grouping

### Meeting (10/06/2024) - Task Timeline and Effort Matrix
- Submitted task timeline with deadlines
- Created team member effort matrix for project components
- Started setting up development environment and repository structure

### Meeting (10/13/2024) - Requirements and Technical Specifications
- Submitted comprehensive requirements document
- Defined technical specifications including:
  - Data structures for user representation
  - Machine learning approach for clustering
  - API endpoints for frontend interaction
  - Integration patterns with Spotify API

### Meeting (10/27/2024) - Oral Project Presentations
- Submitted videos of oral project presentations
- Demonstrated initial system architecture
- Outlined planned implementation strategy

### Meeting (11/03/2024) - Fall Design Reports
- Submitted Fall Design Reports to faculty advisor
- Received assessment feedback for all team members
- Established development priorities for winter break

### Meeting (11/17/2024) - Frontend Prototype and Authentication
- Implemented basic frontend with HTML templates
- Set up Spotify OAuth authentication flow
- Created initial Flask routes for user login
- Tested authentication process with Spotify API

## Winter Break Development (Dec 2024 - Jan 2025)
- Refined front-end components and user interface
- Implemented initial data structures for user profiles
- Created utility functions for genre analysis
- Established development workflow for spring semester

## Spring Semester 2025

### Meeting (01/13/2025) - Core Data Structures & Project Adaptation
- Addressed critical issue: Spotify's API deprecated most song-specific endpoints
- Pivoted project approach to focus on genre distribution analysis instead
- Implemented `User` class in `user.py` with genre-based profile structure
- Created functions to parse Spotify track data into genre categories
- Set up genre cache system to reduce API calls and improve performance

### Meeting (01/20/2025) - Local Data Storage Planning
- Designed data storage structure for the application
- Created prototype data models for users, playlists, and tracks
- Implemented temporary file-based storage solution
- Began research on AWS DynamoDB integration for future implementation

### Meeting (01/27/2025) - Clustering Algorithm
- Implemented initial clustering system in `clustering.py`
- Created placeholder functions for user cluster assignment
- Defined cosine similarity metrics for genre vectors
- Implemented supergenre classification system

### Meeting (02/03/2025) - Test Plan Documentation & Machine Learning Implementation
- Submitted comprehensive test plan with unit tests and integration strategy
- Established metrics for evaluating clustering performance
- Implemented `Clusterer` class with K-means algorithm
- Switched from cosine similarity to Euclidean distance for improved clustering results
- Created prediction methods and training matrix generation for user classification

### Meeting (02/10/2025) - User Documentation & Playlist Generation System
- Submitted user documentation with features guide and troubleshooting section
- Documented data privacy considerations for application users
- Implemented playlist analysis functionality in `playlist_utils.py`
- Created genre distribution extraction from playlists
- Implemented track URI collection for playlist creation

### Meeting (02/17/2025) - Slidedeck Documentation & Recommendation Engine
- Completed presentation slides with system architecture diagrams
- Created visualizations of clustering results for presentation
- Enhanced playlist recommendation system with similarity-based generation
- Added weighting system for cluster-based recommendations
- Created three playlist types: most similar, expand horizons, and discovery

### Meeting (03/03/2025) - DynamoDB Integration
- Completed `DynamoDBHandler` class implementation
- Created AWS DynamoDB table structures for users, playlists, and tracks
- Implemented data conversion for DynamoDB compatibility
- Added CRUD operations for user profile data
- Enhanced Flask application routes to use database storage

### Meeting (03/10/2025) - Optimization and Refinement
- Improved clustering algorithm performance
- Optimized database access patterns
- Enhanced caching for genre data
- Refined similarity metrics for better recommendations

### Meeting (03/17/2025) - Expo Poster
- Finalized expo poster design
- Included key technical achievements
- Added visual representations of system architecture
- Prepared QR codes for live demonstration

### Meeting (03/24/2025) - Poster and Video Preparation
- Finalized poster with latest system metrics
- Created demonstration video showing key system features
- Prepared talking points for expo presentations
- Rehearsed demonstration flow for Tech Expo

### Meeting (03/31/2025) - System Finalization
- Completed final testing of entire system
- Fixed remaining bugs and performance issues
- Prepared live demonstration environment
- Created backup systems for expo presentation

## CEAS Tech Expo (04/08/2025)
- Successfully demonstrated system to faculty and industry professionals
- Presented working prototype with real-time user clustering
- Showcased playlist generation based on user taste profiles
- Received positive feedback on implementation and innovation

### Meeting (04/14/2025) - Final Report and Project Retrospective
- Submitted final comprehensive project report
- Completed peer reviews of team contributions
- Conducted team retrospective on project achievements and challenges
- Documented lessons learned and opportunities for future enhancements
- Officially concluded the senior design project