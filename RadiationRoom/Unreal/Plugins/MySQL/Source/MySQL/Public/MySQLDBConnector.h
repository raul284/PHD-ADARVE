// Copyright 2021-2022, Athian Games. All Rights Reserved. 

#pragma once

#include "CoreMinimal.h"
#include "UObject/NoExportTypes.h"

#include "MySQLBPLibrary.h"
#include "DLLManager.h"

#include "MySQLDBConnector.generated.h"

/**
 * 
 */
UCLASS()
class MYSQL_API UMySQLDBConnector : public UObject
{
	GENERATED_BODY()

private:

	UMySQLDBConnector();
	

public:

	bool bIsConnectionBusy;


	bool CreateNewConnection(FString Server, FString DBName, FString UserID, FString Password, TMap<FString, FString> ExtraParams,
		FString& ErrorMessage);
	
	void  CloseConnection();

	void UpdateDataFromQuery(FString Query, bool& IsSuccessful, FString& ErrorMessage);
	;

	void SelectDataFromQuery(FString Query, bool& IsSuccessful, FString& ErrorMessage,
		TArray<FMySQLDataTable>& ResultByColumn, TArray<FMySQLDataRow>& ResultByRow);


	void UpdateImageFromPath(FString Query, FString UpdateParameter, int ParameterID, FString ImagePath, bool& IsSuccessful, FString& ErrorMessage);
	UTexture2D* SelectImageFromQuery(FString Query, FString SelectParameter, bool& IsSuccessful, FString& ErrorMessage);

};
