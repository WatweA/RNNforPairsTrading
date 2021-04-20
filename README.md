## Pairwise Stock Prediction
##### Team - Daniel Krasnonosenkikh and Aaditya Watwe

## Problem Description
We’re hoping to replicate a pair-wise long-short equity strategy for a basket of stocks traded on the NASDAQ and NYSE. This strategy entails finding closely correlated equities, and categorizing whether the first equity in the pair will outperform the other in the future day/week/month. The returns from this strategy are lower than buy-and-hold but the direction (up or down) of the market as a whole will not influence our returns. Based on the predicted future return ratio from our model, we will take a long position in the pair’s first asset and a short position in the other, if the future ratio is greater than 1. If the ratio is less than 1 we simply flip these positions. Thus all of the return we earn from the model will be based on the effectiveness of the model we select in predicting the ratio between the selected assets.

For more details see: [Project Proposal](https://github.com/WatweA/RNNforPairsTrading/blob/main/project/proposal.md)

Please fork and expand on our project: [LICENSE](https://github.com/WatweA/RNNforPairsTrading/blob/main/LICENSE)
