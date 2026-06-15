# DonorConnect

A Cloud-Based Donation & Fundraising Management System built using Flask, MySQL, HTML, CSS and AWS.

---

## Project Overview

DonorConnect is a web-based platform designed to help organizations efficiently manage donors, fundraising campaigns, donations, and reports from a centralized dashboard.

The system provides an easy-to-use admin interface for managing donor information, monitoring campaigns, tracking donations, generating reports, and visualizing cloud deployment architecture.

---

## Features

### Dashboard
- View total donors
- View total campaigns
- View total donations
- View active campaigns
- Quick action buttons
- Recent donation tracking

### Donor Management
- Add new donors
- Search donors
- Edit donor information
- Delete donor records
- Track donation amounts

### Campaign Management
- Create fundraising campaigns
- Set target amounts
- Define start and end dates
- Track campaign progress
- Edit campaign details
- Delete campaigns

### Reports Dashboard
- Total donors statistics
- Total campaigns statistics
- Total donations analytics
- Average donation calculations

### AWS Architecture View
- Users
- Route 53 DNS
- Application Load Balancer
- EC2 Flask Server
- RDS MySQL Database
- S3 File Storage
- CloudWatch Monitoring

### Security Features
- Protected admin login
- Session-based authentication
- Secure database connectivity

---

## Technology Stack

### Frontend
- HTML5
- CSS3
- Jinja2 Templates

### Backend
- Python
- Flask

### Database
- MySQL

### Cloud Services
- AWS EC2
- AWS RDS
- AWS S3
- AWS Route 53
- AWS CloudWatch

### Version Control
- Git
- GitHub

---

## Project Structure

```text
donorconnect/
│
├── templates/
│   ├── dashboard.html
│   ├── donors.html
│   ├── campaigns.html
│   ├── reports.html
│   ├── architecture.html
│   ├── edit_donor.html
│   ├── edit_campaign.html
│   └── login.html
│
├── static/
│
├── app.py
├── db.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Dashboard Modules

### Dashboard
Provides a complete overview of platform activity.

### Donors
Stores and manages donor records.

### Campaigns
Manages fundraising campaigns and targets.

### Reports
Displays donation and campaign analytics.

### Architecture
Shows AWS cloud deployment architecture.

---

## Database Design

### Donors Table

| Field | Type |
|---------|---------|
| id | INT |
| name | VARCHAR |
| email | VARCHAR |
| phone | VARCHAR |
| city | VARCHAR |
| amount_donated | DECIMAL |

---

### Campaigns Table

| Field | Type |
|---------|---------|
| id | INT |
| title | VARCHAR |
| description | TEXT |
| target_amount | DECIMAL |
| raised_amount | DECIMAL |
| start_date | DATE |
| end_date | DATE |

---

## Installation Guide

### Clone Repository

```bash
git clone https://github.com/Chandresh111/donorconnect.git
```

### Move into Project

```bash
cd donorconnect
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

#### Windows

```bash
venv\Scripts\activate
```

#### Mac/Linux

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Application

```bash
python app.py
```

---

## Future Enhancements

- Email notifications
- Payment gateway integration
- Donor certificates
- PDF report generation
- Campaign image uploads
- Donation receipts
- User role management
- Real-time analytics
- Interactive charts
- Mobile responsive design

---

## Learning Outcomes

Through this project:

- Built a complete Flask web application
- Implemented CRUD operations
- Connected Flask with MySQL
- Designed responsive dashboards
- Managed Git and GitHub workflows
- Learned AWS cloud architecture
- Applied full-stack development concepts

---

## Author

**Chandresh Dubey**

B.Tech Computer Science Engineering

GitHub:
https://github.com/Chandresh111

---

## License

This project is created for educational and learning purposes.

© 2026 DonorConnect. All Rights Reserved.