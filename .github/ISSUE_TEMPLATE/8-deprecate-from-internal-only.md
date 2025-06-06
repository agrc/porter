---
name: (🔐 UGRC internal use) Internal/Open SGID only deprecation
about: Data is being removed from Internal/Open SGID but preserved in AGOL.
title: Remove <thing> from Internal/Open SGID while preserving in AGOL
labels: "deprecation, porter"
assignees: "@steveoh, @eneemann, @rkelson"
---

## Summary

<!-- conductor = {"table":""} -->

- **Internal Dataset Name**: SGID.<category>.<dataset>
- **External Dataset Name**:
- **ArcGIS Online Url**:

_A short summary of the situation._

### Migration Guide

_A short summary of how users affected by this deprecation can modify their workflows and projects to continue to get similar or improved functionality_

<!-- this is here to help the writing juices flow. feel free to completely replace this or simply fill in the blanks -->

This dataset has been removed from internal and Open SGID but can still be access in the SGID on ArcGIS.

### Action items

1. _Assign a person who should complete the task by replacing `name` with their github `@name`._
1. _Check [x] the box when the task is completed and add the date of completion._
1. _~Strike~ out all items that do not apply._

- [ ] Prevent forklift from updating the AGOL Item from Internal by updating the "AGOL_ITEM_ID" field in the META.AGOLItems table to be "hosted by UGRC" (name, completed: `2025/00/00`)
- [ ] Update the [SGID Index](https://docs.google.com/spreadsheets/d/11ASS7LnxgpnD0jN4utzklREgMf1pcvYjcXcIcESHweQ/edit#gid=1024261148) update "storageType" to be "AGOL". (name, completed: `2025/00/00`)
- [ ] Check if this layer in the base maps. If so, work with Zach to develop a path forward before you proceed with a Hard Delete (name, completed: `2025/00/00`).
- [ ] Add "Backup" tag to AGOL Item so that it is backed up by [Moonwalk](https://github.com/agrc/project-moonwalk) (name, completed: `2025/00/00`)
- [ ] Manually remove data from the Internal SGID (name, completed: `2025/00/00`)
- [ ] Remove Farm from AGOL connection (forklift) (name, completed: `2025/00/00`)
- [ ] Update relevant [gis.utah.gov](https://gis.utah.gov/products/sgid/categories/) product pages (including `downloadMetadata.ts` and `public/_redirects`) (name , completed: `2025/00/00`)
- [ ] Delete Google Drive data (name, completed: `2025/00/00`)
- [ ] Remove row from `SGID.META.ChangeDetection` (name, completed: `2025/00/00`) (it was already gone)
- [ ] Remove data from forklift hashing and receiving (name, completed: `2025/00/00`)
- [ ] Remove row from `data/hashed/changedetection.gdb/TableHashes` (name, completed: `2025/00/00`)
- [ ] Remove data from record series with archives (name, completed: `2025/00/00`)

#### Static

- [ ] Upload to appropriate `UtahAGRC/{SGID Category}` folder in AGOL (for `shelved` datasets) (name, completed: `2025/00/00`)

### :robot: Automation validation

1. _Assign yourself or someone to check the item by replacing `name` with their github `@name`._
1. _Check [ ] the box and add the date of verification `2025/01/01` when the task is verified._
1. _~Strike~ out all items that do not apply._

- [ ] Remove data from Open SGID (name on `2025/00/00`)
- [ ] [sgid-index](https://gis.utah.gov/products/sgid/sgid-index/) (name on `2025/00/00`)
- [ ] Auditor sets appropriate `static` information (name on `2025/00/00`)

### Are there service dependencies

- [ ] Are clients querying this data with the UGRC API search endpoint? [This dashboard](https://lookerstudio.google.com/reporting/fbfcf1d5-e9c2-4b8a-94ae-9529d5d0bbef/page/p_7k74ao7wjd) may be helpful.
- [ ] Notify Don Jackson (don.jackson1 at motorolasolutions.com) if the data is in the Next-Generation 911 Motorola Aware Map? (name on `2025/00/00`)
- [ ] Does any other application depend on this data? (name on `2025/00/00`)
  - dependency 1

### Notification

- [ ] X (@steveoh)

### Group Task Assignments

1. _Check [ ] the box when you have assigned all the tasks relevant to your group._

- [ ] Data Team (@eneemann)
- [ ] Dev Team (@steveoh)
- [ ] Cadastre Team (@rkelson)
