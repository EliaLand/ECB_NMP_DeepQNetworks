# ECB NMP DeepQNetworks

The ECB manages an extensive and complex real estate portfolio across multiple jurisdictions. Periodically the respective property managers provide a control sheet presenting a global overview of the respective invoices that has been processed throughout the reference period. The CRE team is in charge of initiating the verification workflow and this latter has historically been handled manually, depending on the approach of individual property managers.

<div align="center">
<img src="Images/MB-3D.png" alt="System Architecture" width="500"/>


<div align="left">

  
# **NAVIGATION**

  The interface includes a sidebar with navigation buttons to switch between sections:

  - **Home**
  - **NMP Invoice Checker**
  - **Info**

  ---

# **HOME**

  The Home section is the default landing page.  
  It displays the ECB logo and the title **“NMP INVOICE CHECKER”**.

  ---

# **NMP INVOICE CHECKER**

  This section is divided into four main steps.

  ## Upload Your Control File

  1. Open **NMP Invoice Checker** from the sidebar.
  2. Click on **CONTROL FILE**.
  3. Upload your control Excel file (`.xlsx` or `.csv`).
  4. Select the columns you want to display.
  5. The selected columns are shown in a table.

  ## Upload Your Invoices

  1. Click on **INVOICES**.
  2. Upload invoice files in **PDF format**.
  3. Invoice text is extracted and tokenized automatically.

  ## Invoice Verification

  1. Click on **VERIFICATION**.
  2. Select the matching criteria from the control file columns.
  3. Map the following fields:
  - **Invoice Number**
  - **Supplier**
  - **Amount**
  4. Click **Launch invoice verification**.

  The verification results are displayed in a table.

  ## Validation

  This section allows you to review and validate the verification results.

  ---

# **INFO**

  The Info section provides general information about the application  
  and includes a chatbot for user assistance.
      """
