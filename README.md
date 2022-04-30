# How to use

Basically the most important thing is to configurate correctly this scipt. So let's dive in config.ini file.

### Params
This segment relates to the parameters of the parsing data. 
> is_proportionally
>
You can tell the script exactly how you want to split tokens between the wallets, because it may be a situation where the division will not be uniform, for example, not 1:1:1:1, but 1:2:6:3 (how to do this I will tell below), in which case you need to put opposite of this parameter **1**. If you want to do the division evenly, put **0**.

> is_amount_in_gwei 
>
This parameter indicates whether or not the amount of tokens to split is specified in gwei. If you specified an amount that you would normally see in wallets such as MetaMask (for example, you might have 1.2 BNB), then you should assign this parameter **0**. If you know that your token amount is in uint format, then write **1**.
> path_to_wallets
>
The path to the .txt file with the list of wallets where the tokens will be sent. The default is wallets.txt file inside the directory. I don't see the point in changing it, but it may come in handy.