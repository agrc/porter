# Porter

A porter is person that

- carries things, such as bags
- performs routine cleaning, likely on a train, taking care of the sleeping berths.

UGRC tracks the additions, replacements, and deletions of SGID items (in the broadest sense of add, replace, or delete) through issues in this repository.

## How to use

1. [Create a new issue](https://github.com/agrc/porter/issues/new/choose) when an application, dataset, or both needs to be added, deleted, or moved to a different long-term storage
1. Choose the `Removing Data From Anywhere` (for moving or deleting data) or `Introduce data to the SGID` (for adding data) template from the buttons
1. Tag the three triagers (one from each team) in the triage section:
   - [ ] Data Team Triage (@gregbunce)
1. The triagers will choose which items need to be handled and tag the appropriate people to handle them:
   - [ ] ArcGIS Online (@jacobdadams)
   - Items that don't need to be handled should be struck through (wrap the line with `~`'s) instead of being deleted:
     - `~ArcGISOnline (assigned to)~` (note there are no spaces between the `~`'s and the text to be struck out)
   - Once the triager has identified any steps required for their team or made any relevant comments, they should check the box in the triage section to indicate that their triage is complete:
     - [x] Data Team Triage (@gregbunce)
1. The people assigned to different issues will check the boxes as they are completed and comment on the issue to notify the rest of the group:
   - [x] ArcGIS Online (@jacobdadams)
1. Once all boxes are checked, the person who first opened the issue should close it.

## Task Completion Dates

Porter issue templates include task lines with placeholder completion dates, such as:

- [ ] Data Team Triage (name, completed: `2026/00/00`)
- [ ] Validation review (name on `2026/00/00`)

When one of these Porter task lines is checked in an issue description, GitHub Actions automatically replaces the placeholder date with the current date in the `America/Denver` timezone.

This automation only updates Porter-style checked task lines that still contain a placeholder date. It does not update unchecked tasks, struck-through tasks, or tasks that already have a real completion date. If a box is unchecked later, the existing completion date is left in place.

## Data Flow for New SGID Datasets

If there is a record added to `SGID.META.AGOLItems`, the corresponding dataset will automatically be added to:

1. the open sgid with cloudb
1. arcgis online with forklift
1. open data with the agol validator

Note: cloudb is the only automation from the list above that works in reverse. If a record is removed from `SGID.META.AGOLItems`, the corresponding data needs to be manually removed from all of the systems above with the exception of the Open SGID.

### Tweet templates

#### intent to deprecate

```md
🚮🗑️🚮 Deprecation Notice 🚮🗑️🚮

[Dataset]

https://github.com/agrc/porter/issues/#

#utmap #ugrcporter
```

#### issue completed

```md
🚮🗑️🚮 Deprecation Complete 🚮🗑️🚮

[Dataset]

https://github.com/agrc/porter/issues/#

#utmap #ugrcporter
```

#### intent to add

```md
🌱🌱The SGID is growing🌳🌳

Dataset from Agency coming soon!

https://github.com/agrc/porter/issues/#

Follow along and comment if you are interested!

#utmap #ugrcporter
```

#### addition complete

```md
🌱🌱The SGID has grown🌳🌳

Dataset from Agency is live in the SGID!

https://github.com/agrc/porter/issues/#

#utmap #ugrcporter
```

## Attribution

This project was developed with the assistance of [GitHub Copilot](https://github.com/features/copilot).
