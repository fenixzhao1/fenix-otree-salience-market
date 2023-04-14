from .models import Constants, Subsession
from ._builtin import Page, WaitPage


class WelcomePage(Page):
    def is_displayed(self):
        return self.round_number == 1


class Instruction(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {
            'state_independent': self.subsession.state_independent,
            'num_states': self.subsession.num_states,
            'num_assets': self.subsession.num_assets
        }


class WaitStart(WaitPage):
    body_text = 'Waiting for all players to be ready'
    wait_for_all_groups = True

    def is_displayed(self):
        return self.round_number <= self.subsession.num_rounds


class Market(Page):
    timeout_seconds = 60
    form_model = 'player'
    form_fields = ['asset_a_bid','asset_a_ask']

    @staticmethod
    def error_message(values):
        if values['asset_a_bid'] > values['asset_a_ask']:
            return 'For Asset A, your bid must be lower than your ask.'

    def is_displayed(self):
        return self.round_number <= self.subsession.num_rounds

    def vars_for_template(self):
        return {
            'round_number': self.round_number,
            'number_of_player': len(self.group.get_players()),
            'p1': self.subsession.p1 * 100,
            'p2': self.subsession.p2 * 100,
            'p3': self.subsession.p3 * 100,
            'asset_a_return_1': self.subsession.x + self.subsession.G,
            'asset_a_return_2': self.subsession.x,
            'asset_a_return_3': self.subsession.x - self.subsession.L,
            'asset_b_return_1': self.subsession.x - self.subsession.G,
            'asset_b_return_2': self.subsession.x,
            'asset_b_return_3': self.subsession.x + self.subsession.L,
            'num_states': self.subsession.num_states,
            'num_assets': self.subsession.num_assets,
            'is_practice': self.subsession.practice,
            'state_independent': self.subsession.state_independent,
            'asseta_endowments': self.subsession.asseta_endowments,
            'assetb_endowments': self.subsession.assetb_endowments,
            'cash_endowments': self.subsession.cash_endowment
        }


class RoundResults(Page):
    timeout_seconds = 30

    def is_displayed(self):
        return self.round_number <= self.subsession.num_rounds

    def vars_for_template(self):
        return {
            'state_a': self.subsession.state_a,
            'state_b': self.subsession.state_b,
            'asset_a_unit': self.player.get_endowments()[0],
            'asset_a_return': self.subsession.get_asset_return('A'),
            'asset_a_total_return': self.player.get_endowments()[0] * self.subsession.get_asset_return('A'),
            'settled_cash': self.player.get_endowments()[2],
            'payoff': self.player.compute_payoff(),
            'state_independent': self.subsession.state_independent,
            'num_assets': self.subsession.num_assets,
            'investor_a': self.subsession.investor_price_a,
        }


class FinalResults(Page):
    def is_displayed(self):
        return self.round_number == self.subsession.num_rounds

    def vars_for_template(self):
        r = self.subsession.get_selected_round()
        player = self.player.in_round(r)
        return {
            'selected_round': r,
            'payoff': player.compute_payoff()
        }


class Questionnaire(Page):
    form_model = 'player'
    form_fields = ['question_1', 'question_2']

    def is_displayed(self):
        return self.round_number == self.subsession.num_rounds


class Demographic(Page):
    form_model = 'player'
    form_fields = ['first_name', 'last_name', 'gender', 'email', 'student_id', 'part_id',
                   'venmo_id', 'comments', 'strategy']

    def is_displayed(self):
        return self.round_number == self.subsession.num_rounds


page_sequence = [WelcomePage, Instruction,
                 WaitStart, Market, RoundResults, Questionnaire, Demographic, FinalResults]
