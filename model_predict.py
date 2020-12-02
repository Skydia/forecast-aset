def predict(df):
    latest_period = 60
    from datetime import timedelta
    from sklearn.preprocessing import RobustScaler
    from tensorflow.keras.models import load_model
    import pandas as pd
    import numpy as np
    
    df['Date'] = pd.to_datetime(df['Date'])

    # Setting the index
    df.set_index('Date', inplace=True)
    
    scaler = RobustScaler()
    scaled_close = scaler.fit_transform(df[['Close']].values)
    df['Close'] = scaled_close
    
    close_scaler = RobustScaler()
    close_scaler.fit(df[['Close']])
    
    checkpoint_path = './tf_server/model_cp'
    model = load_model(checkpoint_path)

    # Predicting off of the most recent days from the original DF
    yhat = model.predict(np.array(df.tail(latest_period)).reshape(1, latest_period, 1))

    # Transforming the predicted values back to their original format
    yhat = close_scaler.inverse_transform(yhat)[0]

    # Creating a DF of the predicted prices
    preds = pd.DataFrame(yhat, 
                         index=pd.date_range(start=df.index[-1]+timedelta(days=1), 
                                             periods=len(yhat), 
                                             freq="B"), 
                         columns=[df.columns[0]]).reset_index()
    preds = preds.rename_axis('Date').reset_index()
    return preds