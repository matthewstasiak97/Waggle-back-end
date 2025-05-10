# Project Description

## Waggle

Waggle is a full‑stack CRUD application that brings local shelter pets right to your fingertips. By aggregating up‑to‑date profiles—from playful pups to cuddly kittens—Waggle makes it effortless to discover and connect with your perfect furry companion. Whether you’re browsing photos, reading bios, or submitting an adoption inquiry, Waggle streamlines the entire process so every pet finds a loving home.

## MVP (Minimum Viable Product) User Stories

1. Authentication & Profiles

As a new user, I want to sign up and log in so I can favorite pets and submit adoption inquiries.

As a guest, I want to browse all adoptable pets without logging in, but need to create an account to save favorites or apply.

2. Pet Discovery & Filtering

As an adopter, I want to see a gallery or list of all available pets, with thumbnail, name, age, and breed.

As an adopter, I want to filter and search by species (dog, cat, etc.), breed, age range, or location so I can find the perfect match.

3. Adoption Inquiries

As a logged‑in user, I want to fill out an inquiry to adopt a pet I have interest in bringing hom.

As a logged‑in user, I want to click “Inquire” on a pet’s profile to send a message or adoption request to the shelter.

4. Edit My Pets and Pending Adoption Inquiries

As a User, I would like to be able to edit my current adopted pets as well as my pending inquires for if I have a change of heart about adopting.

5. Responsive UI & Feedback

As any user, I want clear success/error messages when I create, update, delete, favorite, or inquire—so I know my action went through.

As a mobile user, I want a responsive layout that adapts to phones and tablets so I can browse and apply on the go.

## Stretch Goals

- Develop Shelter View to be fully functional to work in continuity with users looking to adopt.

- Appointment Scheduling & Calendar Sync
  As an adopter, I want to book an in‑person meet‑and‑greet appointment with a pet, complete with date/time slots and email/calendar invites.
  As a shelter admin, I want to approve or reschedule incoming appointment requests and see a daily calendar view of visits.

- Pet Health & History Portal
  As an adopter, I want to view a pet’s vaccination records, medical history, and behavioral assessments in one consolidated timeline.
  As a shelter admin, I want to upload or update health documents and note follow‑up recommendations.

- Analytics Dashboard for Shelters
  As a shelter director, I want real‑time metrics on listing views, inquiry rates, and adoption turnaround times so I can identify bottlenecks and celebrate successes.
  As a volunteer coordinator, I want reports on volunteer impact (hours logged, pets walked, social posts made) to recognize top contributors.

# Timeline - Daily Accountability

| Day       |     | Task                                                       | Blockers | Notes/ Thoughts |
| --------- | --- | ---------------------------------------------------------- | -------- | --------------- |
| Thursday  |     | Create timeline, team guidelines, ERD, proposal, wireframe |          |                 |
| Friday    |     | Finish planning, get proposal approved, Start back-end     |          |                 |
| Saturday  |     | Continue working on back-end                               |          |                 |
| Monday    |     | Back-end completed, start working on Front-End             |          |                 |
| Tuesday   |     | Continue Working on Front-End                              |          |                 |
| Wedensday |     | Continue working on Front-End, Implement CSS               |          |                 |
| Thursday  |     | Finish Front-end and styling. Deploy App via Railway       |          |                 |
| Friday    |     | Present Waggle                                             |          |                 |

---

## ERD

## ![ERD](./public/Images/Waggle-ERD.png)

## Wire Frame

## ![User-View](./public/Images/Wireframe-1.png)

## ![User-View-2](./public/Images/Wireframe-2.png)

## ![User-View-3](./public/Images/Wireframe-3.png)

## ![Shelter-View-1](./public/Images/Wireframe-4.png)

## ![Shelter-View-2](./public/Images/Wireframe-5.png)

## ![Shelter-View-3](./public/Images/Wireframe-6.png)

## Component Hierarchy

## ![Component-Hierarchy](./public/Images/Component-Hierarchy.png)

| Method   | Path                    | Description                              |
| -------- | ----------------------- | ---------------------------------------- |
| `POST`   | `/sign-in`              | Submits login credentials                |
| `POST`   | `/sign-up`              | Submits new user data                    |
| `POST`   | `/signout`              | Handles user logout and redirect         |
| `GET`    | `/pets`                 | View all pets                            |
| `POST`   | `/pets`                 | Create New Pet                           |
| `GET`    | `/pets/:id`             | Retrieve one pet                         |
| `PUT`    | `/pets/:id`             | Update one Pet                           |
| `DELETE` | `/pets/:id`             | Remove a Pet                             |
| `GET`    | `/adoption-inquiry`     | Populate all pending inquiries           |
| `POST`   | `/adoption-inquiry`     | Submits adoption inquiry                 |
| `GET`    | `/adoption-inquiry/:id` | Populate one pending inquiry             |
| `PUT`    | `/adoption-inquiry/:id` | Update pending inquiry                   |
| `DELETE` | `/adoption-inquiry/:id` | Delete one pending inquiry               |
| `GET`    | `*`                     | Fallback for undefined routes (404 page) |
