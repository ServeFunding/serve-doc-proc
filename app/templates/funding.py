TEMPLATES: dict[str, dict] = {
    "merchant_application": {
        "description": "Merchant funding application — populates Deal record",
        "questions": {
            # Business Profile
            "business_name": "What is the legal business name?",
            "dba": "What is the DBA (doing business as) name?",
            "business_state": "What state is the business located in?",
            "client_industry": "What industry or type of business is this?",
            "time_in_business": "How long has the business been operating, or what is the business start date?",
            "monthly_revenue": "What is the stated monthly revenue or gross sales, in USD?",
            "business_structure": "What is the business structure (Sole Proprietorship, LLC, S Corp, C Corp, Partnership, etc.)?",
            "ownership": "What is the ownership percentage breakdown, if listed?",
            "primary_contact_name": "What is the primary contact or owner's full name?",
            "primary_contact_email": "What is the primary contact's email address?",
            "primary_contact_phone": "What is the primary contact's phone number?",
            # Credit & Financial Health
            "credit_score": "What is the owner's credit score, if listed?",
            "existing_funding_positions": "Does the applicant have existing funding positions? If so, what position (1st, 2nd, 3rd+)?",
            "position_sought": "What funding position is being sought (1st, 2nd, 3rd+)?",
            "tax_liens": "Are there any tax liens? If yes, what is the amount?",
            "judgements": "Are there any judgments? If yes, what is the amount?",
            "prior_defaults": "Are there any prior defaults? If yes, how many months ago?",
            "bankruptcy_history": "Is there any bankruptcy history (none, discharged, dismissed, active)? If discharged or dismissed, how many months ago?",
        },
    },
    "bank_statement": {
        "description": "Bank statement analysis for underwriting",
        "questions": {
            "account_holder_name": "What is the account holder name?",
            "bank_name": "What is the bank name?",
            "account_number_last4": "What are the last 4 digits of the account number?",
            "statement_period": "What is the statement period (start and end dates)?",
            "ending_balance": "What is the ending balance?",
            "average_daily_balance": "What is the average daily balance?",
            "total_deposits": "What is the total deposits for the period?",
            "monthly_deposit_count": "How many individual deposits were made during the period?",
            "total_withdrawals": "What is the total withdrawals for the period?",
            "nsf_overdraft_count": "How many NSF or overdraft fees are shown?",
            "negative_balance_days": "How many days did the account have a negative balance?",
        },
    },
    "lender_rate_sheet": {
        "description": "Lender program guide, rate sheet, or guidelines document",
        "questions": {
            # Lender Information
            "lender_name": "What is the lender or funding company name?",
            "lender_website": "What is the lender's website URL?",
            "submission_preference": "How does the lender prefer submissions — via portal or email?",
            "submission_email": "What is the email address for deal submissions?",
            "portal_link": "What is the ISO portal link or URL?",
            # Loan Products
            "products_offered": "What funding products does this lender offer (e.g. Revenue Based Funding, Equipment Financing, Asset Based Line, Invoice Factoring, Purchase Order Financing, Inventory Financing, E-Commerce Financing, SaaS/Recurring Revenue Funding, Commercial Real Estate, Debt Consolidation, SBA Loan)?",
            "loan_type": "Does this lender offer term loans, lines of credit, or both?",
            # Deal Size & Pricing
            "min_funding_amount": "What is the minimum funding amount, in USD?",
            "max_funding_amount": "What is the maximum funding amount, in USD?",
            "app_only_limit": "What is the application-only approval limit (no additional docs needed)?",
            "max_term_length": "What is the maximum term length offered?",
            "pricing_model": "What pricing model is used (factor rate, payback multiple, or fees)?",
            "buy_rate": "What is the buy rate or buy rate range?",
            "max_upsell_rate": "What is the maximum upsell rate or range?",
            "origination_fee": "What is the origination fee or fee range?",
            # Position & Structure
            "positions_funded": "What positions does this lender fund (1st, 2nd, 3rd, 4th, 5th+)?",
            "max_open_positions": "What is the maximum number of open positions allowed?",
            "max_payoff_positions": "How many existing positions will the lender consolidate or pay off?",
            "min_net_funding_required": "What is the minimum net funding required after payoffs?",
            "min_net_renewal_pct": "What minimum percentage of renewal funds must be netted?",
            "ucc_filing_policy": "Does the lender file a UCC lien? If so, under what conditions?",
            # Repayment Terms
            "payment_frequency": "What payment frequencies are accepted (daily, weekly, bi-weekly, semi-monthly, monthly)?",
            "interest_only_payments": "Are interest-only payments available?",
            "prepayment_discounts": "What prepayment discounts are offered (none, partial, cascading, 100% interest forgiveness)?",
            "prepayment_discount_pct": "What is the prepayment discount percentage?",
            "early_payoff_eligible_pct": "After what percentage paid in is the borrower eligible for early payoff?",
            # Business Criteria
            "min_monthly_revenue": "What is the minimum monthly revenue required, in USD?",
            "min_time_in_business": "What is the minimum time in business required?",
            "restricted_industries": "What industries are restricted or excluded?",
            "states_excluded": "What states are excluded from funding?",
            "sole_proprietors_allowed": "Are sole proprietors allowed?",
            "foreign_owners_accepted": "Are foreign owners accepted?",
            "home_based_accepted": "Are home-based businesses accepted?",
            # Credit & Financial Health
            "min_credit_score": "What is the minimum credit score required?",
            "credit_quality": "What credit quality tiers does this lender serve (A, B, C, D)?",
            "personal_guarantee": "What type of personal guarantee is required (full personal guarantee, bad boy guarantee, or none)?",
            "bankruptcy_policy": "What is the lender's policy on bankruptcies?",
            "tax_lien_policy": "What is the lender's policy on tax liens (not allowed, allowed if paid, allowed unpaid)?",
            "judgement_policy": "What is the lender's policy on judgments (not allowed, allowed if paid, allowed unpaid)?",
            "prior_default_policy": "What is the lender's policy on prior defaults (not allowed, allowed, case by case)?",
            # Cash Flow & Bank Activity
            "min_avg_daily_balance": "What is the minimum average daily balance required, in USD?",
            "min_monthly_deposits": "What is the minimum number of monthly deposits required?",
            "max_negative_days": "What is the maximum number of negative balance days allowed per month?",
            "max_nsf_days": "What is the maximum number of NSF/overdraft days allowed per month?",
            # Docs Required
            "bank_statements_required": "Are bank statements required? If so, how many months?",
            "financial_statements_required": "Are financial statements required?",
            "tax_returns_required": "Are tax returns required?",
            "pfs_required": "Are personal financial statements (PFS) required?",
            "lender_application_required": "Is the lender's own application required?",
            # Other
            "unique_features": "What unique features or special programs does this lender offer?",
        },
    },
    "lender_term_sheet": {
        "description": "Lender offer or term sheet for a specific deal",
        "questions": {
            # Lender info
            "lender_name": "What is the lender or funding company name?",
            "lender_id": "What is the lender ID or reference number?",
            # Offer details
            "offer_amount": "What is the approved or offered funding amount, in USD?",
            "factor_rate": "What is the factor rate or payback multiple?",
            "buy_rate": "What is the buy rate?",
            "origination_fee": "What is the origination fee or percentage?",
            "term_length": "What is the term length (in months or years)?",
            "payment_frequency": "What is the payment frequency (daily, weekly, bi-weekly, monthly)?",
            "payment_amount": "What is the regular payment amount?",
            "total_payback": "What is the total payback amount?",
            # Position & structure
            "position": "What position is being funded (1st, 2nd, 3rd, etc.)?",
            "prepayment_discount": "Is there a prepayment discount offered? If so, what are the terms?",
            "interest_only_payments": "Are interest-only payments available?",
            "personal_guarantee": "Is a personal guarantee required?",
            "ucc_filing": "Does the lender file a UCC lien?",
            # Product type
            "product_type": "What type of funding product is this (RBF, term loan, line of credit, equipment financing, etc.)?",
            "loan_type": "Is this a term loan or line of credit?",
        },
    },
    "closing_document": {
        "description": "Funding closing / settlement document",
        "questions": {
            "deal_name": "What is the deal name or reference?",
            "client_name": "What is the client or merchant name?",
            "lender_name": "What is the lender or funding company name?",
            "funded_amount": "What is the funded amount, in USD?",
            "closing_date": "What is the closing or funding date?",
            "commission_rate": "What is the commission rate or percentage?",
            "commission_amount": "What is the commission amount, in USD?",
            "clawback_terms": "What are the clawback terms or conditions, if any?",
            "payoff_amount": "What is the payoff amount for any existing positions?",
            "net_funding": "What is the net funding amount after payoffs?",
        },
    },
    "commission_statement": {
        "description": "Commission payment or remittance statement",
        "questions": {
            "lender_name": "What is the lender or funding company name?",
            "payment_date": "What is the payment or remittance date?",
            "commission_paid": "What is the total commission amount paid, in USD?",
            "payment_method": "What is the payment method (ACH, wire, check)?",
            "invoice_id": "What is the invoice or reference number?",
            "deal_references": "What deal names or IDs are listed on this statement?",
            "is_clawback": "Does this statement indicate a clawback or chargeback?",
            "clawback_amount": "If there is a clawback, what is the clawback amount?",
        },
    },
}


def get_template(name: str) -> dict | None:
    return TEMPLATES.get(name)


def list_templates() -> dict[str, dict]:
    return TEMPLATES
