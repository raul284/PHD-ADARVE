// Copyright 2021-2022, Athian Games. All Rights Reserved. 

#include "DLLManager.h"
#include "Interfaces/IPluginManager.h"

#if PLATFORM_WINDOWS

static void *v_dllHandle;

typedef char*(*_OpenFileDialogue)(char* DialogueTitle, char* FileTypes, bool multiselect);

typedef bool(*_CreateConnection)(int ConnectionID, char* Server, char* DBName, char* UserID, char* Password, char* EparamMap, const char*& ErrorMessage);
typedef void(*_CloseConnection)(int ConnectionID);

typedef bool(*_UpdateDataFromQuery)(int ConnectionID, char* Query, const char*& ErrorMessage);
typedef bool(*_SelectDataFromQuery)(int ConnectionID, char* Query, char* TempDirectory, const char*& ErrorMessage);

typedef bool(*_UpdateImageFromPath)(int ConnectionID, char* Query, char* ImageChar, const char*& ErrorMessage);
typedef bool(*_SelectImageFromQuery)(int ConnectionID, char* Query, char* SelectParameter, const char*& ImageChar, const char*& ErrorMessage);


_OpenFileDialogue m_OpenFileDialogueFromDll;
_CreateConnection m_CreateConnectionFromDll;
_UpdateDataFromQuery m_UpdateDataFromQueryFromDll;
_SelectDataFromQuery m_SelectDataFromQueryFromDll;
_CloseConnection m_CloseConnectionFromDll;

_UpdateImageFromPath m_UpdateImageFromPathFromDll;
_SelectImageFromQuery m_SelectImageFromQueryFromDll;

static FString GetFilePath(FString DLLName)
{
	//Checks for the Plugin path from the current plugin directory. 
	FString Pluginpath = IPluginManager::Get().FindPlugin(TEXT("MySQL"))->GetBaseDir();
	FString DllPath = FPaths::Combine(*Pluginpath, TEXT("Libraries"), DLLName);

	if (FPaths::FileExists(DllPath))
	{
		return DllPath;
	}
	else
	{
		return "";
	}
	
}

bool DLLManager::LoadDLL(FString DLLName)
{
	FString DllPath = GetFilePath(DLLName);

	if (FPaths::FileExists(DllPath))
	{
		v_dllHandle = FPlatformProcess::GetDllHandle(*DllPath);
		if (v_dllHandle != nullptr)
		{
			return true;
		}
	}
	return false;
}

void DLLManager::UnLoadDLL()
{
	if (v_dllHandle != nullptr)
	{
		FPlatformProcess::FreeDllHandle(m_OpenFileDialogueFromDll);
		FPlatformProcess::FreeDllHandle(m_CreateConnectionFromDll);
		FPlatformProcess::FreeDllHandle(m_UpdateDataFromQueryFromDll);
		FPlatformProcess::FreeDllHandle(m_SelectDataFromQueryFromDll);
		FPlatformProcess::FreeDllHandle(m_CloseConnectionFromDll);

		FPlatformProcess::FreeDllHandle(v_dllHandle);
		v_dllHandle = nullptr;
		m_OpenFileDialogueFromDll = nullptr;
		m_CreateConnectionFromDll = nullptr;

	}
}

template<typename T>
bool ImportMethod(FString methodname, T& method)
{
	if (v_dllHandle != NULL)
	{
		method = (T)FPlatformProcess::GetDllExport(v_dllHandle, *methodname);
		if (method)
		{
			return true;
		}
	}
	return false;

}



TArray<FString> DLLManager::GetSplitStringArray(FString Input, FString Pattern)
{

	TArray<FString> Results;

	FString Base;
	FString Left;
	FString Remaining;

	if (Input.Split(Pattern, &Base, &Remaining))
	{
		Results.Add(Base);

		while (Remaining != "")
		{
			if (Remaining.Split(Pattern, &Left, &Remaining))
			{
				Results.Add(Left);
			}
			else
			{
				Results.Add(Remaining);
				Remaining = "";
			}
		}

	}
	else
	{
		Results.Add(Input);

	}

	return Results;

}

TArray<FString> DLLManager::GetOpenFileDialogue(FString DialogueTitle, FString FileTypes, bool multiselect)
{
	TArray<FString> OpenedFiles;
	if (ImportMethod<_OpenFileDialogue>("OpenFileDialogue", m_OpenFileDialogueFromDll))
	{

		char* title = TCHAR_TO_ANSI(*DialogueTitle);
		char* filetypes = TCHAR_TO_ANSI(*FileTypes);

		char* openedfilename = m_OpenFileDialogueFromDll(title, filetypes, multiselect);

		FString RString = FString(openedfilename);
		if (!RString.IsEmpty())
		{
			FString LString;
			while (!RString.IsEmpty())
			{
				FString NString = RString;
				RString.Empty();
				if (NString.Contains(","))
				{
					NString.Split(",", &LString, &RString, ESearchCase::CaseSensitive);
				}
				else
				{
					LString = NString;
				}
				if (FPaths::FileExists(LString))
				{
					OpenedFiles.Add(LString);
				}
			}


		}
	}

	return OpenedFiles;
}



bool DLLManager::UpdateImageFromPath(int ConnectionID, FString Query, FString ImagePath, FString& ErrorMessage)
{

	if (ImportMethod<_UpdateImageFromPath>("UpdateImageFromPath", m_UpdateImageFromPathFromDll))
	{
		
		string query(TCHAR_TO_UTF8(*Query));
		char* querychar = _strdup(query.c_str());

		char* ImageChar = UMySQLBPLibrary::GetRawImageFromPath(ImagePath);

		const char* errormessage = "";
		bool UpdateStatus = m_UpdateImageFromPathFromDll(ConnectionID, querychar, ImageChar, errormessage);
		ErrorMessage = FString(UTF8_TO_TCHAR(errormessage));

		return UpdateStatus;
	}
	
	return false;
}

UTexture2D* DLLManager::SelectImageFromQuery(int ConnectionID, FString Query, FString SelectParameter, FString& ErrorMessage)
{
	if (ImportMethod<_SelectImageFromQuery>("SelectImageFromQuery", m_SelectImageFromQueryFromDll))
	{
		string query(TCHAR_TO_UTF8(*Query));
		char* querychar = _strdup(query.c_str());

		string selectparameter(TCHAR_TO_UTF8(*SelectParameter));
		char* selectparameterchar = _strdup(selectparameter.c_str());
		
		const char* ichar = "";
		const char* errormessage = "";

		if(bool SelectStatus = m_SelectImageFromQueryFromDll(ConnectionID, querychar, selectparameterchar, ichar, errormessage))
		{
			char* ImageChar = const_cast<char*>(ichar);
			FString ImageString  = FString(UTF8_TO_TCHAR(ichar));
			UTexture2D* ImageTexture = UMySQLBPLibrary::LoadTexturefromCharData(ImageChar);
			return ImageTexture;
		}
		else
		{
			ErrorMessage = FString(UTF8_TO_TCHAR(errormessage));
		}
	
	}
	return nullptr;
}



bool DLLManager::CreateConnection(int ConnectionID, FString Server, FString DBName, FString UserID, FString Password, TMap<FString, FString> ExtraParams,
	FString& ErrorMessage)
{
	if (ImportMethod<_CreateConnection>("CreateConnection", m_CreateConnectionFromDll))
	{

		string titlestring(TCHAR_TO_UTF8(*Server));
		char* title = _strdup(titlestring.c_str());

		string dbnamestring(TCHAR_TO_UTF8(*DBName));
		char* dbname = _strdup(dbnamestring.c_str());

		string useridstring(TCHAR_TO_UTF8(*UserID));
		char* userid = _strdup(useridstring.c_str());

		string passwordstring(TCHAR_TO_UTF8(*Password));
		char* password = _strdup(passwordstring.c_str());

		string Eparamstring;

		for (auto eParam : ExtraParams)
		{
			char* eparamkey(TCHAR_TO_UTF8(*eParam.Key));
			char* eparamvalue(TCHAR_TO_UTF8(*eParam.Value));

			string EparamKey(eparamkey);
			string EparamValue(eparamvalue);

			Eparamstring += EparamKey + "," + EparamValue + ";";
		}

		char* eparamstring = _strdup(Eparamstring.c_str());

		const char* errormessage = "";
		bool connectionpropertystate = m_CreateConnectionFromDll(ConnectionID, title, dbname, userid, password, eparamstring, errormessage);


		ErrorMessage = FString(UTF8_TO_TCHAR(errormessage));
		return connectionpropertystate;

	}

	return false;
}

void DLLManager::CloseConnection(int ConnectionID)
{
	if (ImportMethod<_CloseConnection>("CloseConnection", m_CloseConnectionFromDll))
	{
		m_CloseConnectionFromDll(ConnectionID);
	}
}


bool DLLManager::UpdateDataFromQuery(int ConnectionID, FString Query, FString& ErrorMessage)
{
	if (ImportMethod<_UpdateDataFromQuery>("UpdateDataFromQuery", m_UpdateDataFromQueryFromDll))
	{
		string query(TCHAR_TO_UTF8(*Query));
		char* q = _strdup(query.c_str());

		const char* errormessage = "";
		bool UpdateStatus = m_UpdateDataFromQueryFromDll(ConnectionID, q, errormessage);
		ErrorMessage = FString(UTF8_TO_TCHAR(errormessage));

		return UpdateStatus;

	}

	return false;
}

bool DLLManager::SelectDataFromQuery(int ConnectionID, FString Query, FString& ErrorMessage, TArray<FMySQLDataTable>& ResultByColumn, TArray<FMySQLDataRow>& ResultByRow)
{
	if (ImportMethod<_SelectDataFromQuery>("SelectDataFromQuery", m_SelectDataFromQueryFromDll))
	{
		string query(TCHAR_TO_UTF8(*Query));
		char* q = _strdup(query.c_str());

		const char* errormessage = "";

		FString UserDirectory = FPaths::ConvertRelativePathToFull(FPaths::ProjectDir());
		string udstring(TCHAR_TO_UTF8(*UserDirectory));
		char* udir = _strdup(udstring.c_str());

		bool SelectStatus = m_SelectDataFromQueryFromDll(ConnectionID, q, udir, errormessage);
		ErrorMessage = FString(UTF8_TO_TCHAR(errormessage));

		if (SelectStatus)
		{

			FString ColumnNamesPath = FPaths::Combine(UserDirectory, TEXT("SelectColumnNames.txt"));
			if (FPaths::FileExists(ColumnNamesPath))
			{
				FString ColumnNames = "";
				FFileHelper::LoadFileToString(ColumnNames, *ColumnNamesPath, FFileHelper::EHashOptions::EnableVerify);

				FString* LeftS = &ColumnNames;
				FString* RightS = nullptr;

				TArray<FString> ColumnNamesArray = GetSplitStringArray(ColumnNames, "<&&columnbreak>");
				for (auto& ColumnName : ColumnNamesArray)
				{

					FMySQLDataTable NewDataTable;
					NewDataTable.ColumnName = ColumnName;
					ResultByColumn.Add(NewDataTable);

				}

			}

			FPlatformFileManager::Get().GetPlatformFile().DeleteFile(*ColumnNamesPath);

			FString ColumnDataPath = FPaths::Combine(UserDirectory, TEXT("SelectColumnData.txt"));
			if (FPaths::FileExists(ColumnDataPath))
			{
				FString ColumnData = "";
				FFileHelper::LoadFileToString(ColumnData, *ColumnDataPath, FFileHelper::EHashOptions::EnableVerify);

				TArray<FString> RowDataArray = GetSplitStringArray(ColumnData, "<&&rowbreak>");

				for (auto& rowdata : RowDataArray)
				{
					FMySQLDataRow Row;
					TArray<FString> ColumnDataArray = GetSplitStringArray(rowdata, "<&&columnbreak>");
					for (auto& cdata : ColumnDataArray)
					{
					    int32 CIndex = ColumnDataArray.IndexOfByKey(cdata);
						if (ResultByColumn.Num() > CIndex)
						{
							ResultByColumn[CIndex].ColumnData.Add(cdata);
						}
						Row.RowData.Add(cdata);

					}


					ResultByRow.Add(Row);

				}


			}

			FPlatformFileManager::Get().GetPlatformFile().DeleteFile(*ColumnDataPath);


		}
		
		return SelectStatus;

	}

	return false;
}


#endif
