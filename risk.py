from database import get_cursor

conditions = ['heart', 'birth']


def get_risk(age, sex):
    return {
        cond: get_risk_for_condition(cond, age, sex)
        for cond in conditions
    }


def get_risk_for_condition(condition, age, sex):
    cur = get_cursor()

    cur.execute(
        "SELECT IF(MIN(rate) IS NULL, 0, rate) AS rate FROM conditions "
        "WHERE year = 2012 AND age = %s AND sex = %s "
        "AND `condition` = %s", (age, sex, condition))
    data = cur.fetchone()

    return data[0]
