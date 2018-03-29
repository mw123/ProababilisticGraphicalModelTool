# myPGM

I implemented a simple Bayes net toolbox, which allows construction of discrete Bayesian networks. This toolbox contains two types of inference algorithms: Variable Elimination and Gibbs Sampling. 

The API for using myPGM toolbox is shown in test_gibbs_sampler.ipynb and test_variable_elimination.ipynb. In these two IPython notebooks, inference results from myPGM are compared to that of pgmpy, which is a Python library for working with probabilistic graphical models.