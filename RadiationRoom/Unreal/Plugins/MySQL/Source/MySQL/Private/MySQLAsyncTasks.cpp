// Copyright 2021-2022, Athian Games. All Rights Reserved. 


#include "MySQLAsyncTasks.h"
#include "MySQLDBConnectionActor.h"
#include "MySQLBPLibrary.h"


OpenConnectionTask::OpenConnectionTask(AMySQLDBConnectionActor* dbConnectionActor, UMySQLDBConnector* dbConnector, FString server, FString dBName, FString userID, FString password, TMap<FString, FString> extraParams)
{
	Server = server;
	DBName = dBName;
	UserID = userID;
	Password = password;
	ExtraParams = extraParams;
	CurrentDBConnectionActor = dbConnectionActor;
	MySQLDBConnector = dbConnector;
}

OpenConnectionTask::~OpenConnectionTask()
{

}


void OpenConnectionTask::DoWork()
{

	if (MySQLDBConnector)
	{
		FString ErrorMessage;
		bool ConnectionStatus = MySQLDBConnector->CreateNewConnection(Server, DBName, UserID, Password, ExtraParams, ErrorMessage);
		AMySQLDBConnectionActor* dbConnectionActor = CurrentDBConnectionActor;

		AsyncTask(ENamedThreads::GameThread, [dbConnectionActor, ConnectionStatus, ErrorMessage]()
		{
			if (dbConnectionActor && dbConnectionActor->IsValidLowLevel())
			{
				dbConnectionActor->bIsConnectionBusy = false;
				dbConnectionActor->OnConnectionStateChanged(ConnectionStatus, dbConnectionActor->CurrentConnectionID, ErrorMessage);
				dbConnectionActor->CurrentConnectionID = dbConnectionActor->CurrentConnectionID + 1;

			}
			
		});

	}
	
}



UpdateQueryAsyncTask::UpdateQueryAsyncTask(AMySQLDBConnectionActor* dbConnectionActor, UMySQLDBConnector* dbConnector, TArray<FString> queries)
{
	Queries = queries;
	CurrentDBConnectionActor = dbConnectionActor;
	MySQLDBConnector = dbConnector;

}

UpdateQueryAsyncTask::~UpdateQueryAsyncTask()
{

}

void UpdateQueryAsyncTask::DoWork()
{
	bool UpdateQueryStatus = true;;
	FString ErrorMessage;

	if (MySQLDBConnector)
	{
		for (int iIndex = 0; iIndex < Queries.Num(); iIndex++)
		{
			bool CurrentUpdateQueryStatus = false;
			FString CurrentErrorMessage;
			MySQLDBConnector->UpdateDataFromQuery(Queries[iIndex], CurrentUpdateQueryStatus, CurrentErrorMessage);
			
			if (!CurrentUpdateQueryStatus)
			{
				UpdateQueryStatus = false;
				ErrorMessage = CurrentErrorMessage;
			}
		}
		
	}
	else
	{
		ErrorMessage = "InValid Connection";
		UpdateQueryStatus = false;
	}

	AMySQLDBConnectionActor* dbConnectionActor = CurrentDBConnectionActor;
	AsyncTask(ENamedThreads::GameThread, [dbConnectionActor, UpdateQueryStatus, ErrorMessage]()
	{
		if (dbConnectionActor && dbConnectionActor->IsValidLowLevel())
		{

			dbConnectionActor->bIsConnectionBusy = false;
			dbConnectionActor->OnQueryUpdateStatusChanged(UpdateQueryStatus, ErrorMessage);
		}
	});
	
}


SelectQueryAsyncTask::SelectQueryAsyncTask(AMySQLDBConnectionActor* dbConnectionActor, UMySQLDBConnector* dbConnector, FString query)
{
	Query = query;
	CurrentDBConnectionActor = dbConnectionActor;
	MySQLDBConnector = dbConnector;

}

SelectQueryAsyncTask::~SelectQueryAsyncTask()
{

}

void SelectQueryAsyncTask::DoWork()
{
	FString ErrorMessage;
	bool SelectQueryStatus;
	TArray<FMySQLDataTable> ResultByColumn;
	TArray<FMySQLDataRow> ResultByRow;

	if (MySQLDBConnector)
	{
		MySQLDBConnector->SelectDataFromQuery(Query, SelectQueryStatus, ErrorMessage, ResultByColumn, ResultByRow);
	}
	else
	{
		ErrorMessage = "InValid Connection";
		SelectQueryStatus = false;
	}

	AMySQLDBConnectionActor* dbConnectionActor = CurrentDBConnectionActor;
		
	AsyncTask(ENamedThreads::GameThread, [dbConnectionActor, SelectQueryStatus, ErrorMessage, ResultByColumn, ResultByRow]()
	{
		if (dbConnectionActor && dbConnectionActor->IsValidLowLevel())
		{
			dbConnectionActor->bIsConnectionBusy = false;
			dbConnectionActor->OnQuerySelectStatusChanged(SelectQueryStatus, ErrorMessage, ResultByColumn, ResultByRow);
		}
	});
	
}


UpdateImageAsyncTask::UpdateImageAsyncTask(AMySQLDBConnectionActor* dbConnectionActor, UMySQLDBConnector* dbConnector, FString query, FString updateParameter, int parameterID, FString imagePath)
{
	Query = query;
	UpdateParameter = updateParameter;
	ParameterID = parameterID;
	ImagePath = imagePath;
	CurrentDBConnectionActor = dbConnectionActor;
	MySQLDBConnector = dbConnector;

}

UpdateImageAsyncTask::~UpdateImageAsyncTask()
{

}

void UpdateImageAsyncTask::DoWork()
{
	bool UpdateQueryStatus;
	FString ErrorMessage;

	if (MySQLDBConnector)
	{
		 MySQLDBConnector->UpdateImageFromPath(Query, UpdateParameter, ParameterID, ImagePath, UpdateQueryStatus, ErrorMessage);
	}
	else
	{
		ErrorMessage = "InValid Connection";
		UpdateQueryStatus = false;
	}
	

	AMySQLDBConnectionActor* dbConnectionActor = CurrentDBConnectionActor;
	AsyncTask(ENamedThreads::GameThread, [dbConnectionActor, UpdateQueryStatus, ErrorMessage]()
		{
			if (dbConnectionActor && dbConnectionActor->IsValidLowLevel())
			{

				dbConnectionActor->bIsConnectionBusy = false;
				dbConnectionActor->OnImageUpdateStatusChanged(UpdateQueryStatus, ErrorMessage);
			}

		});
}


SelectImageAsyncTask::SelectImageAsyncTask(AMySQLDBConnectionActor* dbConnectionActor, UMySQLDBConnector* dbConnector, FString query, FString selectParameter)
{
	Query = query;
	SelectParameter = selectParameter;
	CurrentDBConnectionActor = dbConnectionActor;
	MySQLDBConnector = dbConnector;

}

SelectImageAsyncTask::~SelectImageAsyncTask()
{

}

void SelectImageAsyncTask::DoWork()
{
	bool SelectQueryStatus;
	FString ErrorMessage;
	UTexture2D* SelectedTexture = nullptr;

	if (MySQLDBConnector)
	{
		SelectedTexture = MySQLDBConnector->SelectImageFromQuery(Query, SelectParameter, SelectQueryStatus, ErrorMessage);
	}
	else
	{
		ErrorMessage = "InValid Connection";
		SelectQueryStatus = false;
	}

	
	AMySQLDBConnectionActor* dbConnectionActor = CurrentDBConnectionActor;
	AsyncTask(ENamedThreads::GameThread, [dbConnectionActor, SelectQueryStatus, ErrorMessage, SelectedTexture]()
		{
			if (dbConnectionActor && dbConnectionActor->IsValidLowLevel())
			{
	
				dbConnectionActor->bIsConnectionBusy = false;
				dbConnectionActor->OnImageSelectStatusChanged(SelectQueryStatus, ErrorMessage, SelectedTexture);
			}
		});

}





