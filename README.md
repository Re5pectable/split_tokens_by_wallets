# How to use

## Configuration
Basically the most important thing is to configurate correctly this scipt. So let's dive in **config.ini** file.

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

### Wallet
This segment relates to getting an access to your wallet.
> HTTPprovider
>
It's pretty obvious. The HTTP address of the provider. For example, to work with the wallet inside BEP20 you need https://bsc-dataseed.binance.org/
> chain_id
>
An important detail without which transfers don't work. I recommend going to this site https://chainlist.org/ it has all the list you need. For Binance chain_id is 56.
> gas_limit
>
Gas limit per operation. For BEP20 **200000** is enough.
> wallet
>
Your wallet address.
> secret
>
Secret key for your wallet.

### Token_to_split
> contract
>
The contract of the token you want to split
> amount
> 
Amount of tokens you want to split. This is the option for **which is_amount_in_gwei** was created. 

# Wallets list
To create a list of wallets, use the wallets.txt file and line by line specify all the wallets to which you want to transfer tokens without spaces or empty lines, please pay attention to this. 

If you want an even split, then just list all the wallets and that will be enough. Don't forget only to specify in config is_proportionally=0. 

However, if you want to specify in what proportions the tokens should be sent, then follow the following pattern
> 0x1Address|1
> 0x2Address|2
> 0x3Address|3
>
Get the idea? The address is followed by the | sign and then the proportion from 1 to 999. In my example, the division is 1 to 2 to 3, that is, if I have 6000 tokens, the first address gets 1000, the second 2000, and the third 3000. Simple math: add up all the specified fractions, and divide the total number of tokens by that number.  And then individually multiply by the corresponding proportion. If you are more comfortable with percentages, there is no problem. Specify 10, 20, 70 so that the first wallet gets 10%, the second 20%, and the third 70%. But remember, the input should be numeric, no need to specify the sign of the percentage.