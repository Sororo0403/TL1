#include "Engine.h"
#include "scenes/EditorScene.h"

#include <memory>

int WINAPI wWinMain(HINSTANCE instance, HINSTANCE, PWSTR, int showCommand) {
    EngineRuntimeConfig config{};
    config.width = 1280;
    config.height = 720;
    config.title = L"LevelEditor";

    EngineRuntime runtime;
    return runtime.Run(instance, showCommand, std::make_unique<EditorScene>(),
                       config);
}
