---
name: (🔐 UGRC internal use) SGID addition
about: A new SGID dataset is being proposed for inclusion in the SGID
title: Add <dataset name> from <source>
labels: "introduction, porter"
assignees: "@steveoh, @eneemann, @rkelson"
---

## Summary

<!-- conductor = {"table":"category.internaltablename"} -->

- **Proposed Readable Name**: Utah FooBar <!-- AGOL_PUBLISHED_NAME -->
- **Proposed Internal Dataset Name**: FooBar
- **Proposed External Dataset Name**: foo_bar <!-- AGOL_PUBLISHED_NAME with spaces converted to underscores and Utah removed -->
- **Proposed Data Category**: Quux
- **Data Description**: Bar
- **Source Agency/Entity**: Baz
- **Contact**: Bar Baz
- **Update Frequency**: Quarterly

_Introduce your data, where it comes from, why it is being added etc._

### The data should be available in

1 _Check [x] all the areas where you expect the data to show up._

- [ ] Internal SGID
- [ ] Open SGID
- [ ] ArcGIS Online
- [ ] Open Data

### The data is of high quality

- [ ] Sweeper checks have run and passed (name on `2025/00/00`)
- [ ] The minimum requirements for [metadata](https://gis.utah.gov/about/policy/sgid/) are populated (name on `2025/00/00`)
- [ ] The data complies with our [domain rules](https://gis.utah.gov/about/policy/sgid/) (name on `2025/00/00`)

### Where is the data source

_Choose one._

- [ ] Internal SGID
- [ ] Farm from AGOL ([agol item url](https://<orgname>.maps.arcgis.com/home/item.html?id=<itemid))
- [ ] UGRC AGOL ([agol item url](https://<orgname>.maps.arcgis.com/home/item.html?id=<itemid))

### Action items

1. _Assign a person who should complete the task by replacing `name` with their github `@name`._
1. _Check [x] the box when the task is completed and add the date of completion._
1. _~Strike~ out all items that do not apply._

- [ ] Add data to the [Internal SGID](https://stackoverflow.com/c/ugrc/questions/109) (name, completed: `2025/00/00`)
- [ ] Add new entry to [MATT](https://github.com/agrc/metadata-asset-tracking-tool/tree/main/metadata) (name, completed: `2025/00/00`)
- [ ] Configure forklift for Farm from AGOL (name, completed: `2025/00/00`)
- [ ] Update relevant [gis.utah.gov](https://gis.utah.gov/data) data pages (name, completed: `2025/00/00`)
- [ ] Add a [SGID Index](https://docs.google.com/spreadsheets/d/11ASS7LnxgpnD0jN4utzklREgMf1pcvYjcXcIcESHweQ/edit#gid=1024261148) record (name, completed: `2025/00/00`)
- [ ] Complete a `SGID.META.AGOLItems` record (name, completed: `2025/00/00`)
  - `AGOL_ITEM_ID` will be populated by Forklift after it publishes the new AGOL item.
- [ ] Complete an [AGOLItems_shelved](http://utah.maps.arcgis.com/home/item.html?id=1760fbedbc7e49429aa6c0c3ab1442ec) record for any `static` or `shelved` item (name, completed: `2025/00/00`)
- [ ] Data is assigned to a record series with archives (@eneemann, completed: `2025/00/00`)
- [ ] If data is hosted in AGOL exclusively, add `Backup` tag to hosted feature layer so that it will be backed up by [moonwalk](https://github.com/agrc/project-moonwalk) (name, completed: `2025/00/00`)

### :robot: Automation validation

1. _Assign yourself or someone to check the item by replacing `name` with their github `@name`._
1. _Check [x] the box and add the date of verification `2025/01/01` when the task is verified._
1. _~Strike~ out all items that do not apply._

- [ ] Open SGID via cloudb (@steveoh on `2025/00/00`)
- [ ] ArcGIS Online via forklift (@stdavis on `2025/00/00`)
- [ ] [Auditor](https://github.com/agrc/Auditor) ran successfully (@jacobdadams on `2025/00/00`)
- [ ] [SGID on ArcGIS](https://opendata.gis.utah.gov) (name on `2025/00/00`)
- [ ] [gis.utah.gov](https://gis.utah.gov/products/sgid/categories/) data pages (name on `2025/00/00`)
- [ ] [sgid-index](https://gis.utah.gov/products/sgid/sgid-index/) (@steveoh on `2025/00/00`)

### Notification

- [ ] X (@steveoh)

### Group Task Assignments

1. _Check [x] the box when you have assigned all the tasks relevant to your group._

- [ ] Data Team (@eneemann)
- [ ] Dev Team (@steveoh)
- [ ] Cadastre Team (@rkelson)
