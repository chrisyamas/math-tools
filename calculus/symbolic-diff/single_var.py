from fractions import Fraction
import re


def diff_polynom(expr):
    """
    Input expression cannot contain parentheses/brackets of any kind.
    Bad: 4*(x^2 + x)
    Good: 4*x^2 + 4*x

    Input expression cannot contain more than more variable.
    Bad: 3*x + 5*y
    Good: 3x^2 + 5*x + 1

    Input expression must include at least one whitespace character on both
    sides of an addition or subtraction operator.
    Bad: 7z +2
    Good: 7z + 2
    Bad: 6x^2-5x+1
    Good: 6x^2 - 5x + 1

    :param expr: string, represents polynomial expression
    :return display_string: string, represents first derivative of input expression
    """
    # Convert expr string to lower case to ignore case
    expr = expr.lower()

    trig_set = {"sin", "cos", "tan", "cot", "sinh", "cosh", "tanh"}

    for element in trig_set:
        if element in expr:
            if element == "sin":
                # expr = "sin(x)"
                parts = expr.split("(")
                inside = parts[1].split(")")[0]
                outside_derivative = "cos"
                inside_derivative = diff_polynom(inside)
                full_derivative = f"{outside_derivative}({inside})"
                final_derivative = f"{inside_derivative} * {full_derivative}"
                return final_derivative

    # Checks to ensure expr has no more than one variable
    var_set = set(char for char in expr if char.isalpha())
    if len(var_set) > 1:
        raise ValueError("Expression can only contain one variable")

    # No variables --> derivative of an integer equals zero
    elif len(var_set) == 0:
        return 0

    variable = var_set.pop()

    # Replace subtraction with negative addition
    expr = expr.replace(" - ", " + -")
    terms = [x.strip() for x in expr.split(" + ")]

    num_str = r"\-*\s*[0-9]*\/*[0-9]*"
    co_power_regex = re.compile(rf"({num_str})?\**({variable})?\^*({num_str})?")

    diff_terms = {}
    for term in terms:
        coefficient, term_var, power = co_power_regex.search(term).groups()
        # Handles common writing conventions for "default 1" coefficients
        if not coefficient:
            coefficient = 1
        if coefficient == "-":
            coefficient = -1
        if not term_var:
            # There is only a coefficient; input power = 0, so derivative = 0
            continue
        elif not power or int(power) == 1:
            # Input power = 1, so derivative = value of coefficient
            diff_coefficient = Fraction(coefficient)
            diff_power = 0
        else:
            # Calculates the derivative
            diff_coefficient = Fraction(coefficient) * Fraction(power)
            diff_power = Fraction(power) - 1

        # Reason #1 to use a dictionary for holding the coefficient values:
        #   Combining 'like terms' (coefficients of terms with same power)
        if diff_terms.get(diff_power):
            stored_value = diff_terms.get(diff_power)
            combined_value = diff_coefficient + stored_value
            diff_terms[diff_power] = combined_value
        else:
            diff_terms[diff_power] = diff_coefficient

    display_expr = ""
    # Reason #2 to use a dictionary for holding coefficient values:
    #   Preparing return expression with terms in descending exponent order
    desc_powers = sorted([k for k in diff_terms.keys()], reverse=True)
    for i in range(len(desc_powers)):
        display_power = desc_powers[i]
        display_coefficient = diff_terms[display_power]
        if display_power == 0:
            display_term = f"{display_coefficient}"
        elif display_power == 1:
            display_term = f"{display_coefficient}{variable}"
        else:
            display_term = f"{display_coefficient}{variable}^{display_power}"
        if i == 0:
            display_expr += display_term
        else:
            display_expr += f" + {display_term}"

    return display_expr


if __name__ == "__main__":
    expression = "sin(x)"
    result = diff_polynom(expression)
    print(result)
