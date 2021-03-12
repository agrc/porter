---
name: Removing data from the SGID
about: SGID Deprecation Checklist
title: Remove <dataset name> from SGID
labels: "deprecation, porter"
assignees: "@steveoh, @gregbunce, @rkelson"
---

# Summary

- **Internal Dataset Name**:
- **External Dataset Name**:
- **ArcGIS Online Url**:

_A short summary of the situation._

## Migration Guide

_A short summary of how users affected by this deprecation can modify their workflows and projects to continue to get similar or improved functionality_

<!-- this is here to help the writing juices flow. feel free to completely replace this or simply fill in the blanks -->

This dataset has been replaced by () which is named () in the Open SGID and () in the SGID Open Data.
The replaced data is still accessible via our shelved policy in AGOL (a link to the shelved item).

## Action items

1. _Assign a person who should complete the task by replacing `name` with their github `@name`._
1. _Check [x] the box when the task is completed and add the date of completion._
1. _~Strike~ out all items that do not apply._

### Soft Delete

_The purpose of the soft delete is to ensure that all of our users and applications have gracefully migrated off of the dataset. Soft deletes will remain in effect for 14 days. During this time, you will have the ability to restore the dataset to its original SGID offering(s). Once the 14 pass, the item is then eligible for a hard delete._

If this dataset is being replaced, then wait until the new data is publicly available before completing these steps:

- [ ] Mark ArcGIS Online item as deprecated in preparation for future deletion (name, completed: `2021/00/00`)
  - [ ] Change `Authoritative` field to `d` in `SGID.META.AGOLItems` to set the `Deprecated` AGOL flag (name, completed: `2021/00/00`)
  - [ ] Add note to ArcGIS Online description noting when layer will be deleted and any replacement layer (name, completed: `2021/00/00`)
- [ ] Unshare item from Open Data (name, completed: `2021/00/00`)
- [ ] Remove the SGID Index item (name, completed: `2021/00/00`)
- [ ] Update the `AGOL_ITEM_ID` field in the `SGID.META.AGOLItems` table to a non-GUID text (ie: `Removed from AGOL` or `Replaced by abc from xyz`). Allow this new text to exist though on [Auditor](https://github.com/agrc/auditor) run - Auditor currently runs daily at 5:00am (name, completed: `2021/00/00`)
  - [ ] After one successful Auditor run, remove the row from the `SGID.META.AGOLItems` table (name, completed: `2021/00/00`)

### Hard Delete

_Hard deletes are final. It is recommend to complete the the soft delete process before moving on to these steps. If you decide to skip the soft delete, note that you will need to incorporate some of those steps here._

- [ ] Remove data from the Internal SGID (name, completed: `2021/00/00`)
- [ ] Delete ArcGIS Online item (name, completed: `2021/00/00`)
  - currently achieved by either deleting the AGOL item, changing the `AGOL_ITEM_ID` field in `SGID.META.AGOLItems` to something other than an Item ID and manually removing the item from all SGID groups, or shelving the data.
- [ ] Remove Farm from AGOL connection (name, completed: `2021/00/00`)
- [ ] Update relevant [gis.utah.gov](https://gis.utah.gov/data) data pages (name, completed: `2021/00/00`)
- [ ] Add this porter url to the `Deprecated` field of the [Stewardship](https://docs.google.com/spreadsheets/d/11ASS7LnxgpnD0jN4utzklREgMf1pcvYjcXcIcESHweQ/edit#gid=1) record (name, completed: `2021/00/00`)
- [ ] Update `SGID.META.AGOLItems` table (name, completed: `2021/00/00`)
  - cut and paste row to `AGOLItems_shelved` table if shelving (see below)
  - set the `AGOL_ITEM_ID` field to `hosted by <agency>` for Farm from AGOL
  - set the `AGOL_ITEM_ID` field to `exclude from AGOL` to not publish to ArcGIS Online
- [ ] Delete Google Drive data (name, completed: `2021/00/00`)
- [ ] Remove row from `SGID.META.ChangeDetection` (name, completed: `2021/00/00`)
- [ ] Remove json file from [Backseat Driver](https://github.com/agrc/backseat-driver) (name, completed `2021/00/00`)
- [ ] Remove data from forklift hashing and receiving (name, completed: `2021/00/00`)
- [ ] Remove row from `data/hashed/changedetection.gdb/TableHashes` (name, completed: `2021/00/00`)

### Shelve/Static

_Choose one based on situation._

- [ ] Upload to `UtahAGRC/AGRC_Shelved` folder in AGOL (New shelved item not already in AGOL) (name, completed: `2021/00/00`)
- [ ] Move existing AGOL item to `AGRC_Shelved` AGOL folder (shelving an item already in AGOL) (name, completed: `2021/00/00`)
- [ ] Upload to appropriate `UtahAGRC/{SGID Category}` folder in AGOL (for `static` datasets) (name, completed: `2021/00/00`)

_Add record to table._

- [ ] Add record to `AGOLItems_shelved` [table](https://utah.maps.arcgis.com/home/item.html?id=1760fbedbc7e49429aa6c0c3ab1442ec) in ArcGIS Online  with `shelved` or `static` in the `CATEGORY` field (name, completed: `2021/00/00`)

## :robot: Automation validation

1. _Assign yourself or someone to check the item by replacing `name` with their github `@name`._
1. _Check [x] the box and add the date of verification `2020/01/01` when the task is verified._
1. _~Strike~ out all items that do not apply._

- [ ] Remove data from Open SGID (name on `2021/00/00`)
- [ ] [sgid-index](https://gis.utah.gov/data/sgid-index) (@steveoh on `2021/00/00`)
- [ ] Auditor sets appropriate `shelved`/`static`/`Deprecated` information (@jacobdadams on `2021/00/00`)

## Are there service dependencies

- Does an application depend on this data?
- Are clients querying this data with the WebAPI?

## Notification

- [ ] Twitter (@steveoh)

## Group Task Assignments

1. _Check [x] the box when you have assigned all the tasks relevant to your group._

- [ ] Data Team (@gregbunce)
- [ ] Dev Team (@steveoh)
- [ ] Cadastre Team (@rkelson)
