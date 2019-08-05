---
name: Deprecate SGID Dataset or Web Application
about: Deprecation Checklist
title: Deprecate <web app/dataset name>
labels: ''
assignees: ''

---

# Is the data removal temporary or permanent?
- [ ] Replaced with newer data
- [ ] Historical data for archive
- [ ] No longer relevant

# Identify places where the data lives
- [ ] ArcGIS Online
- [ ] Internal SGID
- [ ] External SGID
- [ ] Google Drive 
- [ ] Open data
- [ ] Mapserv
- [ ] gis.utah.gov data pages 
- [ ] Stewardship doc and sgid-index

# Is there a website?
- [ ] Is the source code on GitHub?
- [ ] Should it be archived?
- [ ] Should it be removed from the web server or show a static page with information?
- [ ] Should it redirect somewhere else?

# Is there a map service?
- [ ] Should it be stopped or deleted?

# Is there a forklift pallet?
- [ ] Should it continue to run or be removed?

# Are there service dependencies?
- [ ] Does the web api query it?
- [ ] Do AGRC or applications widgets reference it?
