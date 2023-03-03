// Copyright 2021-2022, Athian Games. All Rights Reserved. 

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "MySQLBPLibrary.h"
#include "MySQLAsyncTasks.h"

#include "MySQLDBConnector.h"

#include "MySQLDBConnectionActor.generated.h"


UCLASS()
class MYSQL_API AMySQLDBConnectionActor : public AActor
{
	GENERATED_BODY()
	
private:


	FAsyncTask<OpenConnectionTask>*   OpenConnectionTaskPtr;
	FAsyncTask<UpdateQueryAsyncTask>* UpdateQueryAsyncTaskPtr;
	FAsyncTask<SelectQueryAsyncTask>* SelectQueryAsyncTaskPtr;
	FAsyncTask<UpdateImageAsyncTask>* UpdateImageAsyncTaskPtr;
	FAsyncTask<SelectImageAsyncTask>* SelectImageAsyncTaskPtr;

public:	
	// Sets default values for this actor's properties
	AMySQLDBConnectionActor();

protected:
	// Called when the game starts or when spawned
	virtual void BeginPlay() override;
	virtual void EndPlay(const EEndPlayReason::Type EndPlayReason) override;

	UMySQLDBConnector* GetConnector(int32 ConnectionID);

public:	

	UPROPERTY()
		bool bIsConnectionBusy;


	UPROPERTY()
		TMap<int32, UMySQLDBConnector*> SQLConnectors;

	UPROPERTY()
		int32 CurrentConnectionID;

	// Called every frame
	virtual void Tick(float DeltaTime) override;

	/**
	* Creates a New Database Connection
	*/
	UFUNCTION(BlueprintCallable, Category = "MySql Server")
		void CreateNewConnection(FString Server, FString DBName, FString UserID, FString Password, TMap<FString, FString> ExtraParams);

	UFUNCTION(BlueprintCallable, Category = "MySql Server")
		void CloseAllConnections();

	UFUNCTION(BlueprintCallable, Category = "MySql Server")
		void CloseConnection(int32 ConnectionID);

	UFUNCTION(BlueprintImplementableEvent, Category = "MySql Server")
		void OnConnectionStateChanged(bool ConnectionStatus, int32 ConnectionID, const FString& ErrorMessage);

	/**
	* Executes a Query to the database
	*/
	UFUNCTION(BlueprintCallable, Category = "MySql Server")
		void UpdateDataFromQuery(int32 ConnectionID, FString Query);

	/**
	* Executes Multiple Queries Simultaneously to the database
	*/
	UFUNCTION(BlueprintCallable, Category = "MySql Server")
		void UpdateDataFromMultipleQueries(int32 ConnectionID, TArray<FString> Queries);

	UFUNCTION(BlueprintImplementableEvent, Category = "MySql Server")
		void OnQueryUpdateStatusChanged(bool IsSuccessful, const FString& ErrorMessage);


	/**
	* Selects data from the database
   */
	UFUNCTION(BlueprintCallable, Category = "MySql Server")
		void SelectDataFromQuery(int32 ConnectionID, FString Query);

	UFUNCTION(BlueprintImplementableEvent, Category = "MySql Server")
		void OnQuerySelectStatusChanged(bool IsSuccessful, const FString& ErrorMessage, const TArray<FMySQLDataTable>& ResultByColumn, 
			const TArray<FMySQLDataRow>& ResultByRow);


	/**
		* Updates image to the database from the hard drive Asynchronously
	*/
	UFUNCTION(BlueprintCallable, Category = "MySql Server")
		bool UpdateImageFromTexture(int32 ConnectionID, FString Query, FString UpdateParameter, int ParameterID, UTexture2D* Texture);

	/**
	* Updates image to the database from the hard drive Asynchronously
	*/
	UFUNCTION(BlueprintCallable, Category = "MySql Server")
		void UpdateImageFromPath(int32 ConnectionID, FString Query, FString UpdateParameter, int ParameterID, FString ImagePath);


	UFUNCTION(BlueprintImplementableEvent, Category = "MySql Server")
		void OnImageUpdateStatusChanged(bool IsSuccessful, const FString& ErrorMessage);


	/**
	* Selects image from the database and returns Texture2D format of the selected image
	*/
	UFUNCTION(BlueprintCallable, Category = "MySql Server")
		void SelectImageFromQuery(int32 ConnectionID, FString Query, FString SelectParameter);

	UFUNCTION(BlueprintImplementableEvent, Category = "MySql Server")
		void OnImageSelectStatusChanged(bool IsSuccessful, const FString& ErrorMessage, UTexture2D* SelectedTexture);



};
