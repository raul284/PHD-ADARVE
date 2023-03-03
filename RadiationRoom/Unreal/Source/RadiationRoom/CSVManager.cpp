// Fill out your copyright notice in the Description page of Project Settings.


#include "CSVManager.h"

void UCSVManager::ReadCSV(FString path, FString filename, bool hasHeader, 
	FString& header, TArray<FString>& data)
{
	fstream file;
	string auxPath = string(TCHAR_TO_UTF8(*path));
	string auxFilename = string(TCHAR_TO_UTF8(*filename));

	file.open(auxPath + "/" + auxFilename, fstream::in);

	if (file) {

		TArray<FString> rows;
		string line;

		while (getline(file, line)) {
			rows.Add(line.c_str());
		}
		file.close();

		header = "";
		if (hasHeader) {
			header = rows[0];
			rows.RemoveAt(0);
		}
		data = rows;
	}
}

void UCSVManager::WriteCSV(FString path, FString filename, 
	FString header, TArray<FString> data) {

	// file pointer
	fstream file;
	string auxPath = string(TCHAR_TO_UTF8(*path));
	string auxFilename = string(TCHAR_TO_UTF8(*filename));

	// opens an existing csv file or creates a new file.
	file.open(auxPath + "/" + auxFilename, ios::out | ios::app);

	TArray<FString> parsedHeader;
	header.ParseIntoArray(parsedHeader, TEXT(","), false);

	if (header.Len() > 0) {
		for (FString col : parsedHeader)
		{
			file << string(TCHAR_TO_UTF8(*col)) << ',';
		}
		file << '\n';
	}

	for (FString row : data) {
		TArray<FString> parsedRow;
		row.ParseIntoArray(parsedRow, TEXT(","), false);

		for (FString col : parsedRow) {
			file << string(TCHAR_TO_UTF8(*col)) << ',';
		}
		file << '\n';
	}
}

void UCSVManager::AddRowToCSV(FString path, FString filename, FString data) {
	// file pointer
	fstream file;
	string auxPath = string(TCHAR_TO_UTF8(*path));
	string auxFilename = string(TCHAR_TO_UTF8(*filename));

	// opens an existing csv file or creates a new file.
	file.open(auxPath + "/" + auxFilename, fstream::out | fstream::app);

	file << string(TCHAR_TO_UTF8(*data));
	file << '\n';

	file.close();
}