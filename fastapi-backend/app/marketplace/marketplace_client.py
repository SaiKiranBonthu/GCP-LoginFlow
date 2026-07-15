class MarketplaceClient:
    @staticmethod
    def get_account(marketplace_token: str):
        
        return {
            "accountId": "account-12345",
            "organization": "Acme Corporation",
            "plan": "Basic",
            "subscriptionState": "ACTIVE",
        }