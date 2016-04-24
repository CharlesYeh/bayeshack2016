import re

from database import get_cursor

conditions = ['heart', 'birth', 'flu', 'diabetes', 'concussion']
costs = [7400, 14000, 7300, 9000, 16000]


def get_risk(age, sex):
    return {
        cond: get_risk_for_condition(cond, age, sex)
        for cond in conditions
    }


def get_risk_for_condition(condition, age, sex):
    cur = get_cursor()

    cur.execute(
        """
        SELECT IF(MIN(rate) IS NULL, 0, rate) AS rate FROM conditions
        WHERE year = 2012 AND age = %s AND sex = %s
        AND `condition` = %s""", (age, sex, condition))
    data = cur.fetchone()

    return data[0]


def get_plan(plan_id, age):
    cur = get_cursor()
    cur.execute(
        """
        SELECT
            rt.IndividualRate AS rate,

            hospital.CoinsInnTier1 AS coins,
            primarycare.CopayInnTier1 AS copay,
            plan.DEHBDedInnTier1Individual AS deduc,

            plan.SBCHavingDiabetesCoinsurance AS diabetes_coins,
            plan.SBCHavingDiabetesCopayment AS diabetes_copay,
            plan.SBCHavingDiabetesDeductible AS diabetes_deduc,

            plan.SBCHavingaBabyCoinsurance AS baby_coins,
            plan.SBCHavingaBabyCopayment AS baby_copay,
            plan.SBCHavingaBabyDeductible AS baby_deduc
        FROM PlanAttributes plan
        JOIN Rate rt ON plan.StandardComponentId = rt.PlanId
        LEFT JOIN BenefitsCostSharing hospital
            ON plan.StandardComponentId = hospital.StandardComponentId
            AND hospital.BenefitName LIKE "Inpatient Hospital Services%%"
        LEFT JOIN BenefitsCostSharing primarycare
            ON plan.StandardComponentId = primarycare.StandardComponentId
            AND primarycare.BenefitName LIKE "Primary Care Visit to Treat an Injury or Illness"
        WHERE
            plan.StandardComponentId = %s
            AND rt.Age = %s
        """,
        [plan_id, age])

    data = cur.fetchone()
    if data is None:
        return {}

    rate = float(data[0])

    coins = data[1]
    copay = data[2]
    deduc = data[3]

    cond_costs = {}
    for cond in conditions:
        if cond == 'diabetes':
            cond_costs[cond] = ({
                'coins_cost': dollarToInt(data[4]),
                'copay': dollarToInt(data[5]),
                'deduc': dollarToInt(data[6]),
            })
        elif cond == 'birth':
            cond_costs[cond] = ({
                'coins_cost': dollarToInt(data[7]),
                'copay': dollarToInt(data[8]),
                'deduc': dollarToInt(data[9]),
            })
        else:
            # general hospital stats
            cond_costs[cond] = ({
                'coins': coinsToFloat(coins),
                'copay': dollarToInt(copay),
                'deduc': dollarToInt(deduc),
            })

    return {
        'rate': rate,
        'conditions': cond_costs
    }


def dollarToInt(dollar):
    return int(dollar[1:].replace(',', ''))


def coinsToFloat(coins):
    match = re.match(r'([0-9]+)% Coinsurance', coins, re.I)

    if match:
        return float(match.group(1)) / 100

    return None
