# Evaluation

I ran the pipeline on two companies — Bharat Forge Limited (a large listed company) and Brakes India Private Limited (a private company with no public stock listing). These two were chosen deliberately because they represent opposite ends of the data availability spectrum. Here is what came out and what I think about it honestly.

---

## Bharat Forge Limited

The output for Bharat Forge is genuinely good. The company overview reads like something an analyst would actually write — it covers the Kalyani Group connection, the global manufacturing footprint across five countries, the BFL 2.0 strategy, and the market cap. Every sentence has a real URL attached to it, not a vague placeholder.

The financial table is the strongest part. Four years of clean data, correct units (₹ Crores), correct currency detection, and the EPS is handled separately so it does not get wrongly converted. The highlights below the table — revenue growth of 36.8% over three years, net income doubling, EBITDA margin improving from 14.9% to 17.6% — are all derived from the actual numbers in the table.

The products section is thorough. It goes beyond just listing categories and actually names specific things — titanium forged flap tracks for Boeing 777X, landing gear components for Embraer, industrial castings through J S Auto Cast. These are not generic descriptions, they are real product relationships pulled from real sources.

The clients section is where the biggest improvement happened compared to earlier versions. It found Boeing, Embraer, Honeywell, General Atomics in aerospace. Daimler, Volkswagen, Toyota, Maruti, Hyundai, Mahindra in automotive. AAM, Dana, Meritor, Valeo in Tier 1 suppliers. Indian Army and Navy with specific contract values. Every client has a source URL.

Where it still falls short — the financial highlights section does some percentage calculations internally (like "36.8% growth" or "104% increase"). That is technically against the no-calculation rule since these numbers are not in the raw Yahoo Finance data, Claude derived them. For an analyst reading this it is useful, but it is a minor inconsistency with the grounding rules.

---

## Brakes India Private Limited

This one is more interesting because it is harder. Brakes India is private, so there is no ticker and no Yahoo Finance table. The pipeline had to find everything from web searches alone.

The company overview came out well. It correctly identified the TSF Group connection, the three divisions (Brake, Foundry, Polymer), the 19 manufacturing facilities across seven states, the international operations in Oman and Indonesia, the 10,000+ employees, and the Deming Prize. All of this is cited.

The financial section is genuinely impressive for a private company. The pipeline found Tofler and CRISIL as sources and pulled five years of data — revenue, operating profit, net profit, margins, ROE, debt metrics, interest coverage. This is real financial data that took some digging to find. The CRISIL rating report was particularly useful and gave details like the debt prepayment in FY2025 and the planned ₹500 crore capex for FY2026.

The products section is detailed and specific — it names actual product lines like the 410 S-cam brake, brake-by-wire actuators, the TVS-Girling and TVS-Apache aftermarket brands, the Qik Brake Service network with 100 centers across 62 cities. This level of detail is genuinely useful.

The clients section found Tata Motors, Maruti Suzuki, Mahindra, Ashok Leyland, Hyundai, Honda, Nissan, Toyota, Volvo, Ford — all with source citations. It even found supplier award relationships like Volvo giving Brakes India a Best Value Product Award in 2011 and Toyota giving a Best Quality Award in 2010.

Where it breaks — some financial metrics are incomplete. EBITDA for example is listed as "decreased 11.29% YoY" without an absolute number because that is all the source had. The pipeline correctly does not invent the number, but it is still a gap. Also the revenue figure of ₹7,499.3 crores for FY2025 does not have a year label in some places — it is clear from context but not perfectly formatted.

The other honest limitation is that for a less well-known private company than Brakes India, this approach would struggle much more. Brakes India has CRISIL reports, Tofler data, and decent press coverage. A smaller private company might have none of that and the financial section would be nearly empty.

---

## Overall Honest Assessment

The pipeline works well for listed companies and better than expected for private ones. The citation grounding is the real strength — every claim points somewhere real. The main remaining weaknesses are that client discovery still depends on how much press coverage exists, financial data for truly obscure private companies will be sparse, and the inline citation format makes the document slightly harder to read for a human even though it is technically correct.
