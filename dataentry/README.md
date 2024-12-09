# **Automate Import/Export**

Automate Import/Export is a Django-based project designed to simplify the import and export of data, leveraging a user-friendly interface and robust backend capabilities.

---

## **Features**
- Upload and process Excel files for importing data.
- Export processed data into downloadable Excel files.
- Email notifications to users upon successful data processing.
- Attach exported files in email notifications.
- Integration with Docker for containerized deployments.

---
## **Technologies Used**
- **Backend**: Django
- **Database**: SQLite
- **Containerization**: Docker, Docker Compose
- **Languages**: Python, HTML
- **Libraries**:
  - Celery
  - Redis
  - python-decouple

---
## **Setup**
### **With Docker**
1. **Build and run Docker containers**:
   ```bash
   docker-compose up --build
---
## **Usage**
- Access the web interface at http://127.0.0.1:8000/.
## **Contribution Guidelines**
- 1.Fork the repository.
- 2.Create a feature branch.
- 3.Write clean, well-documented code.
- 4.Submit a pull request.