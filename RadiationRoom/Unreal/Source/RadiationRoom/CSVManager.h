// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include <iostream>
#include <fstream>
#include <string>
#include <vector>

#include "CoreMinimal.h"
#include "Kismet/BlueprintFunctionLibrary.h"
#include "CSVManager.generated.h"

using namespace std;

/**
 * 
 */
UCLASS()
class RADIATIONROOM_API UCSVManager: public UBlueprintFunctionLibrary
{
	GENERATED_BODY()

public:
	UFUNCTION(BlueprintCallable, category = "CSVManager")
		static void ReadCSV(FString path, FString filename, bool hasHeader, 
			UPARAM(DisplayName = "Header") FString &header, UPARAM(DisplayName = "Data") TArray<FString> &data);

	UFUNCTION(BlueprintCallable, category = "CSVManager")
		static void WriteCSV(FString path, FString filename, 
			FString header, TArray<FString> data);

	UFUNCTION(BlueprintCallable, category = "CSVManager")
		static void AddRowToCSV(FString path, FString filename, FString data);
};
