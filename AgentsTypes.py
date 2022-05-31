from Agents.MEagent import MEagent
import math
import random


# moral licensing -> +
# moral compensation -> -
# dictionary[assignment] = [improvement for me, local changes for neighbours]

# _______________________________________________________________________________________________________________
class SimpleAgent(MEagent):

    # PHASE 2 - Debits - Choose the option that is most beneficial for the society
    def strategy_moral_compensation(self, neighbours_preferences):
        if neighbours_preferences:  # not empty
            criterion = -math.inf
            for assignment in neighbours_preferences:
                social_gain = neighbours_preferences[assignment][1]
                if social_gain > criterion:
                    criterion = social_gain
                    next_assignment = assignment
            return next_assignment
        else:
            return self.assignment

    # PHASE 2 - Credits - Choose the option that is most beneficial to him
    def strategy_moral_licensing(self, beneficial_to_me):
        if beneficial_to_me:  # not empty
            criterion = -math.inf
            for assignment in beneficial_to_me:
                my_gain = beneficial_to_me[assignment][0]
                if my_gain > criterion:
                    criterion = my_gain
                    next_assignment = assignment
            return next_assignment
        else:
            return self.assignment

    def __str__(self):
        s = "I am a Moral-Equilibrium Simple Agent, ID: " + str(self.id) + ", utility: " + str(self.utility) + ", ME: "\
            + str(self.moralEquilibrium) + ", assignment: " + str(self.assignment)
        return s


# _______________________________________________________________________________________________________________
class CarefulAgent(MEagent):

    # PHASE 2 - Debits - from the neighbours’ preferences
    # choose the option that will least distance him from the balance
    def strategy_moral_compensation(self, neighbours_preferences):
        if neighbours_preferences:  # not empty
            criterion = math.inf
            for assignment in neighbours_preferences:
                distance_from_balance = abs(neighbours_preferences[assignment][1].item() + self.moralEquilibrium)
                if distance_from_balance < criterion:
                    criterion = distance_from_balance
                    next_assignment = assignment
            return next_assignment
        else:
            return self.assignment

    # PHASE 2 - Credits - from the options that are beneficial to him
    # choose the option that will least distance him from the balance
    def strategy_moral_licensing(self, beneficial_to_me):
        if beneficial_to_me:  # not empty
            criterion = math.inf
            for assignment in beneficial_to_me:
                distance_from_balance = abs(beneficial_to_me[assignment][1].item() + self.moralEquilibrium)
                if distance_from_balance < criterion:
                    criterion = distance_from_balance
                    next_assignment = assignment
            return next_assignment
        else:
            return self.assignment

    def __str__(self):
        s = "I am a Moral-Equilibrium Careful Agent, ID: " + str(self.id) + ", utility: " + str(self.utility) + \
            ", ME: " + str(self.moralEquilibrium) + ", assignment: " + str(self.assignment)
        return s


# _______________________________________________________________________________________________________________
class GenerousAgent(MEagent):

    # PHASE 2 - Debits - from the neighbours’ preferences
    # Choose the option that is most beneficial for the society
    def strategy_moral_compensation(self, neighbours_preferences):
        if neighbours_preferences:  # not empty
            criterion = -math.inf
            for assignment in neighbours_preferences:
                social_gain = neighbours_preferences[assignment][1].item()
                if social_gain > criterion:
                    criterion = social_gain
                    next_assignment = assignment
            return next_assignment
        else:
            return self.assignment

    # PHASE 2 - Credits - from the options that are beneficial to him
    # choose according to neighbours’ preferences
    def strategy_moral_licensing(self, beneficial_to_me):
        if beneficial_to_me:  # not empty
            criterion = -math.inf
            for assignment in beneficial_to_me:
                social_gain = beneficial_to_me[assignment][1].item()
                if social_gain > criterion:
                    criterion = social_gain
                    next_assignment = assignment
            return next_assignment
        else:
            return self.assignment

    def __str__(self):
        s = "I am a Moral-Equilibrium Generous Agent, ID: " + str(self.id) + ", utility: " + str(self.utility) + \
            ", ME: " + str(self.moralEquilibrium) + ", assignment: " + str(self.assignment)
        return s


# _______________________________________________________________________________________________________________
class SelfishAgent(MEagent):

    # PHASE 2 - Debits - from the neighbours’ preferences, Choose the option that is least harmful for him
    def strategy_moral_compensation(self, neighbours_preferences):
        if neighbours_preferences:  # not empty
            criterion = -math.inf
            for assignment in neighbours_preferences:
                my_gain = neighbours_preferences[assignment][0]
                if my_gain > criterion:
                    criterion = my_gain
                    next_assignment = assignment
            return next_assignment
        else:
            return self.assignment

    # PHASE 2 - Credits - Choose the option that is most beneficial to him
    def strategy_moral_licensing(self, beneficial_to_me):
        if beneficial_to_me:  # not empty
            criterion = -math.inf
            for assignment in beneficial_to_me:
                my_gain = beneficial_to_me[assignment][0]
                if my_gain > criterion:
                    criterion = my_gain
                    next_assignment = assignment
            return next_assignment
        else:
            return self.assignment

    def __str__(self):
        s = "I am a Moral-Equilibrium Selfish Agent, ID: " + str(self.id) + ", utility: " + str(self.utility) + \
            ", ME: " + str(self.moralEquilibrium) + ", assignment: " + str(self.assignment)
        return s


# _______________________________________________________________________________________________________________
class RandomAgent(MEagent):

    # PHASE 2 - Debits - Choose at random from the options that are beneficial for the society
    def strategy_moral_compensation(self, neighbours_preferences):
        if neighbours_preferences:  # not empty
            next_assignment = random.choice(list(neighbours_preferences))
            return next_assignment
        else:
            return self.assignment

    # PHASE 2 - Credits - Choose at random from the options that are beneficial to him
    def strategy_moral_licensing(self, beneficial_to_me):
        if beneficial_to_me:  # not empty
            next_assignment = random.choice(list(beneficial_to_me))
            return next_assignment
        else:
            return self.assignment

    def __str__(self):
        s = "I am a Moral-Equilibrium Random Agent, ID: " + str(self.id) + ", utility: " + str(self.utility) + ", ME: "\
            + str(self.moralEquilibrium) + ", assignment: " + str(self.assignment)
        return s


# _______________________________________________________________________________________________________________
class CalculatedAgent(MEagent):

    # PHASE 2 - Debits - calculate the weigh:
    # how much the assignment will bring me closer to balance and how much he will “pay” for it,
    # choose the with the highest social benefit and minimum harm to the utility
    def strategy_moral_compensation(self, neighbours_preferences):
        if neighbours_preferences:  # not empty
            criterion = -math.inf
            for assignment in neighbours_preferences:
                social_gain = neighbours_preferences[assignment][1].item()
                my_gain = neighbours_preferences[assignment][0]
                if my_gain == 0:
                    my_gain = 0.9
                relative_gain = social_gain / my_gain
                if relative_gain > criterion:
                    criterion = relative_gain
                    next_assignment = assignment
            return next_assignment
        else:
            return self.assignment

    # PHASE 2 - Credits - calculate the weigh:
    # how much the assignment will distance it from balance and how much he will gain from it,
    # choose the assignment with the highest benefit and minimum distance.
    def strategy_moral_licensing(self, beneficial_to_me):
        if beneficial_to_me:  # not empty
            criterion = -math.inf
            for assignment in beneficial_to_me:
                distance_from_balance = abs(beneficial_to_me[assignment][1].item() + self.moralEquilibrium)
                if distance_from_balance == 0:
                    distance_from_balance = 0.9
                my_gain = beneficial_to_me[assignment][0]
                gain_per_distance = my_gain / distance_from_balance
                if gain_per_distance > criterion:
                    criterion = gain_per_distance
                    next_assignment = assignment
            return next_assignment
        else:
            return self.assignment

    def __str__(self):
        s = "I am a Moral-Equilibrium Calculated Agent, ID: " + str(self.id) + ", utility: " + str(self.utility) + \
            ", ME: " + str(self.moralEquilibrium) + ", assignment: " + str(self.assignment)
        return s
