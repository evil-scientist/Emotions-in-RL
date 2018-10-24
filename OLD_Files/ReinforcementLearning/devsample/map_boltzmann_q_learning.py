# -*- coding: utf-8 -*-
from ReinforcementLearning.pyqlearning.qlearning.boltzmann_q_learning import BoltzmannQLearning


class MapBoltzmannQLearning(BoltzmannQLearning):
    '''
    ε-greedy Q-Learning

    Refererence:
        http://d.hatena.ne.jp/Kshi_Kshi/20111227/1324993576

    '''
    
    map = None

    def initialize(self, map):
        self.map = map
        self.t = 1

        for x in range(self.map.width()):
            for y in range(self.map.height()):
                self.save_r_df((x,y), self.map.tileAt(x,y).reward())

    def extract_possible_actions(self, state_key):
        '''
        Concreat method.

        Args:
            state_key       The key of state. this value is point in map.

        Returns:
            [(x, y)]

        '''
        x, y = state_key
        if not self.map.tileAt(x,y).isAccessible():
            raise ValueError("It is the wall. (x, y)=(%d, %d)" % (x, y))

        if self.map.tileAt(x,y).isEndPoint():
            return [self.map.startTuple()]

        around_map = [(x, y-1), (x, y+1), (x-1, y), (x+1, y)]
        possible_actions = []
        for x,y in around_map:
            if self.map.tileAt(x,y).isAccessible():
                possible_actions.append((x,y))
       # print("possible actions: " + str(possible_actions))
        return possible_actions

    def observe_reward_value(self, state_key, action_key):
        '''
        Compute the reward value.
        
        Args:
            state_key:              The key of state.
            action_key:             The key of action.
        
        Returns:
            Reward value.

        '''
        x, y = state_key
        #print("reward: " + str(self.map.tileAt(x,y).reward()))
        return self.map.tileAt(x,y).reward()


    def check_the_end_flag(self, state_key):
        '''
        Check the end flag.
        
        If this return value is `True`, the learning is end.

        Args:
            state_key:    The key of state in `self.t`.

        Returns:
            bool
        '''
        # As a rule, the learning can not be stopped.
        return False

    def normalize_q_value(self):
        '''
        Normalize q-value.
        
        Override.
        
        This method is called in each learning steps.
        
        For example:
            self.q_df.q_value = self.q_df.q_value / self.q_df.q_value.sum()
        '''
        if self.q_df is not None and self.q_df.shape[0] and self.q_df.q_value.max() != self.q_df.q_value.max():
            # min-max normalization
            self.q_df.q_value = (self.q_df.q_value - self.q_df.q_value.min()) / (self.q_df.q_value.max() - self.q_df.q_value.min())

    def normalize_r_value(self):
        '''
        Normalize r-value.

        Override.

        This method is called in each learning steps.

        For example:
            self.r_df = self.r_df.r_value / self.r_df.r_value.sum()
        '''
        if self.r_df is not None and self.r_df.shape[0]:
            # z-score normalization.
            self.r_df.r_value = (self.r_df.r_value - self.r_df.r_value.mean()) / self.r_df.r_value.std()


    def onestep(self, state_key):
        '''
        Learning.
        '''

        #print("self.rdf:")
        #print(self.r_df.to_string())
        next_action_list = self.extract_possible_actions(state_key)
        if len(next_action_list):
            action_key = self.select_action(
                state_key=state_key,
                next_action_list=next_action_list
            )
            reward_value = self.observe_reward_value(state_key, action_key)

        if len(next_action_list):
            # Max-Q-Value in next action time.
            next_state_key = self.update_state(
                state_key=state_key,
                action_key=action_key
            )

            next_next_action_list = self.extract_possible_actions(next_state_key)
            next_action_key = self.predict_next_action(next_state_key, next_next_action_list)
            next_max_q = self.extract_q_df(next_state_key, next_action_key)

            # Update Q-Value.
            self.update_q(
                state_key=state_key,
                action_key=action_key,
                reward_value=reward_value,
                next_max_q=next_max_q
            )
            # Update State.
            #print("uodated state key")
            state_key = next_state_key

        #print("self.qdf: ")
       #print(self.q_df.to_string())


        # Normalize.
        self.normalize_q_value()
        self.normalize_r_value()

        # Epsode.
        self.t += 1
        #print("self.qdf: ")
        #print(self.q_df.to_string())
        #print("self.rdf:")
        #print(self.r_df.to_string())
        return state_key
