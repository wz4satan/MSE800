# Money Exchange System - Project Documentation

This repository contains the core architectural design for the Money Exchange System, defined through two primary functional boundaries: the **Client Portal** and the **Admin Portal**.

---

## 1. Client Portal

### Purpose
This diagram illustrates the core functionalities available to end-users (Customers). It focuses on account management, balance inquiries, and the execution of financial transactions, specifically mapping to the `Transaction` and `Exchange` entities within the system's logic.

### Key Actors
* **Customer:** The primary user initiating financial activities and managing personal funds.
* **Exchange Rate System:** An external system (API) that provides real-time currency data for the `Fetch Exchange Rate` use case.
* **Intermediary Bank:** An external financial institution involved in cross-border or inter-bank transfer processes.

### Relationships
* **Include:**
    * The `Log in` process is mandatory for `View Account Balance`, `Initiate Transaction`, and `Perform Currency Exchange` to ensure secure access.
    * `Perform Currency Exchange` automatically includes `Fetch Exchange Rate` to guarantee transaction accuracy based on current market data.
* **Extend:**
    * `Perform Currency Exchange` serves as a specialized extension of the general `Initiate Transaction` workflow.
    * `Transfer from Intermediary Bank` acts as an optional extension that can be triggered during a currency exchange process under specific conditions.
* **Association:**
    * The `Exchange Rate System` directly supports the `Fetch Exchange Rate` function.
    * The `Intermediary Bank` is interfaced during the `Transfer from Intermediary Bank` business step.

---

## 2. Admin Portal

### Purpose
This diagram outlines the administrative, operational, and compliance functionalities of the software. It demonstrates how internal personnel manage core business entities—such as branches, customer profiles, and accounts—while highlighting critical security and regulatory workflows (KYC and AML).

### Key Actors
* **Branch Staff:** The primary users responsible for day-to-day operations, customer onboarding, and financial monitoring.
* **Anti-Money Laundering (AML) System:** A secondary external actor invoked by the system to perform regulatory compliance checks on high-risk or suspicious transactions.
* **Intermediary Bank:** An external partner bank that facilitates the receipt of incoming remittances.

### Relationships
* **Include:**
    * All administrative actions (`Manage Branch Info`, `Manage Customer Profiles`, `Manage Customer Accounts`, and `Review customer transactions`) require `Staff Login` for auditing and security.
    * The `Review customer transactions` process strictly includes a `Perform KYC check` to maintain regulatory compliance during the audit phase.
* **Extend:**
    * The `Initiate Anti-Money Laundering Check` extends the `Review customer transactions` workflow, triggered automatically if a transaction meets certain risk criteria.
* **Association:**
    * The `AML System` provides the backend validation for the `Initiate Anti-Money Laundering Check`.
    * The `Intermediary Bank` is the primary external entity linked to the `Receive Remittances via Intermediary Bank` use case.

---

## 3. Technical Specifications
* **Security:** A robust authentication-first approach is implemented via mandatory include relationships for all sensitive use cases.
* **Compliance:** KYC (Know Your Customer) and AML (Anti-Money Laundering) workflows are deeply integrated into the administrative review process.
* **External Integration:** The system relies on secure API connections with exchange rate providers, regulatory systems, and partner banks.