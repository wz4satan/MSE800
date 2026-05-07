# Money Exchange System - Client Portal

## Purpose
This diagram illustrates the core functionalities available to the end-users (Customers) of the money exchange system. It focuses on their ability to manage their accounts, view balances, initiate general transactions, and perform specific currency exchanges based on the `Transaction` and `Exchange` entities in the ERD.

## Key Actors
- **Customer:** The primary user initiating financial activities.

- **Exchange Rate API:** A secondary actor providing real-time exchange rates required for the `Exchange` entity.

# Money Exchange System - Admin Portal

## Purpose
This diagram outlines the administrative, operational, and compliance functionalities of the money exchange software. It illustrates how internal personnel interact with the system to manage core business entities, such as maintaining branch details, managing customer profiles, and handling accounts (directly mapping to the Branch, Customer, and Account entities in the ERD). Furthermore, it highlights critical security and regulatory workflows, including mandatory staff authentication, Know Your Customer (KYC) identity verification during account management, and the auditing of Transaction records.

## Key Actors
- **Branch Staff:** The primary internal user responsible for day-to-day branch operations, customer onboarding, and monitoring financial activities.

- **Anti-Money Laundering (AML) System:** A secondary (external) actor that is passively invoked by the system to perform regulatory compliance checks on specific, potentially suspicious transactions.
