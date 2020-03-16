---
name: Deprecate SGID Dataset or Web Application
about: Deprecation Checklist
title: Deprecate <web app/dataset name>
labels: 'deprecation'
assignees: ''

---
# Summary

A short summary of the situation...

<!-- 
1. Delete any action items that you know are not relevant boxes. If in doubt, leave it.
1. Tag anyone who might be a stakeholder in the deprecation.
1. All checkboxes should either be removed or checked before closing the issue.
-->

# Remove data from the following areas

- [ ] ArcGIS Online (intials)
- [ ] Internal SGID (intials)
- [ ] SGID10 (intials)
- [ ] Open SGID (initials)
- [ ] Google Drive (intials)
- [ ] Open data (intials)
- [ ] Mapserv (intials)
- [ ] gis.utah.gov data pages (intials)
- [ ] Stewardship doc and sgid-index (intials)
- [ ] `SGID.META.AGOLItems` (initials)
- [ ] `SGID.META.ChangeDetection` (initials)

# Is there a website?

- [ ] Archive source code repository (intials)
- [ ] Remove from the web server (initials)
or
- [ ] Replace app with a static page with information (intials)
or
- [ ] Redirect somewhere else (intials)

# Is there a map service?

- [ ] Stop (intials)
- [ ] Delete (initials)

# Is there a forklift pallet?

- [ ] Remove repo (intials)
- [ ] Remove stale data from forklift hashing and receiving (initials)

# Are there service dependencies?

- [ ] Validate that the web api does not query it (intials)
- [ ] Validate that AGRC or applications widgets do not reference it (intials)
