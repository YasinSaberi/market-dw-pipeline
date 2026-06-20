CREATE TABLE PipelineLog (
    RunID INT IDENTITY(1, 1) PRIMARY KEY,
    ExecutionStart DATETIME2 NOT NULL,
    ExecutionEnd DATETIME2 NULL, 
    RowsInserted INT DEFAULT 0,
    PipelineStatus VARCHAR(20) CHECK (
        PipelineStatus IN ('RUNNING', 'SUCCESS', 'FAILED') 
    ),
    ErrorMessage VARCHAR(MAX) NULL
);

CREATE TABLE TheCoreMarketDataTable (
    Ticker VARCHAR(10) NOT NULL,
    ObservationDate DATE NOT NULL,
    OpenPrice DECIMAL(10, 2) NULL,  
    HighPrice DECIMAL(10, 2) NULL,
    LowPrice DECIMAL(10, 2) NULL,
    ClosePrice DECIMAL(10, 2) NULL,
    Volume BIGINT NULL,
    IngestedAt DATETIME2 DEFAULT GETDATE(),
    
    CONSTRAINT PK_MarketData PRIMARY KEY (ObservationDate, Ticker)
);