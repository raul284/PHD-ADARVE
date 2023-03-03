// Copyright 2021-2022, Athian Games. All Rights Reserved. 

using UnrealBuildTool;
using System.IO;

public class MySQL : ModuleRules
{

    private string LibrariesPath
    {
        get { return Path.GetFullPath(Path.Combine(ModuleDirectory, "../../Libraries/")); }
    }


    public string BinariesPath
    {

        get { return Path.GetFullPath(Path.Combine(ModuleDirectory, "../../Binaries/Win64/")); }
    }


    public MySQL(ReadOnlyTargetRules Target) : base(Target)
    {

        PrivateIncludePaths.AddRange(new string[]
        {
            "MySQL/Private"

        });


        PCHUsage = ModuleRules.PCHUsageMode.UseExplicitOrSharedPCHs;

        bEnableUndefinedIdentifierWarnings = false;
        bEnableExceptions = true;

        PublicDefinitions.Add("NTDDI_WIN7SP1");

        PublicDependencyModuleNames.AddRange(new[] { "Core", "CoreUObject", "Engine", "RHI",
            "ImageWrapper", "RenderCore", "ImageWriteQueue", "InputCore" , "Projects" });
        PrivateDependencyModuleNames.AddRange(new[] { "XmlParser", "Core", "ImageWrapper", "Engine" });

        if (Target.Platform == UnrealTargetPlatform.Win64)
        {


            PublicDelayLoadDLLs.Add(Path.Combine(LibrariesPath, "FileBrowser.dll"));
            PublicDelayLoadDLLs.Add(Path.Combine(LibrariesPath, "MySQLLibrary.dll"));
            
            PublicDelayLoadDLLs.Add(Path.Combine(BinariesPath, "mysqlcppconn-9-vs14.dll"));
            PublicDelayLoadDLLs.Add(Path.Combine(BinariesPath, "libcrypto-1_1-x64.dll"));
            PublicDelayLoadDLLs.Add(Path.Combine(BinariesPath, "libssl-1_1-x64.dll"));
     
            RuntimeDependencies.Add(Path.Combine(LibrariesPath, "FileBrowser.dll"));
            RuntimeDependencies.Add(Path.Combine(LibrariesPath, "MySQLLibrary.dll"));
            
            RuntimeDependencies.Add(Path.Combine(BinariesPath, "mysqlcppconn-9-vs14.dll"));
            RuntimeDependencies.Add(Path.Combine(BinariesPath, "libcrypto-1_1-x64.dll"));
            RuntimeDependencies.Add(Path.Combine(BinariesPath, "libssl-1_1-x64.dll"));
        }

    }
}