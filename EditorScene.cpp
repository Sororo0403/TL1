#include "scenes/EditorScene.h"

#include "camera/CameraManager.h"

#include <DirectXMath.h>
#include <algorithm>
#include <string>

namespace {

constexpr const char *kEditorCameraName = "EditorCamera";
constexpr const wchar_t *kLevelPath = L"resources/levels/scene.json";

} // namespace

void EditorScene::Initialize(const SceneContext &ctx) {
    BaseScene::Initialize(ctx);

    const int width = ctx.systems.winApp ? ctx.systems.winApp->GetWidth() : 1280;
    const int height = ctx.systems.winApp ? ctx.systems.winApp->GetHeight() : 720;
    const float aspect =
        static_cast<float>(width) / static_cast<float>((std::max)(height, 1));

    if (ctx.systems.cameraManager) {
        Camera &camera =
            ctx.systems.cameraManager->CreateCamera(kEditorCameraName, aspect);
        camera.SetPosition({0.0f, 5.0f, -12.0f});
        camera.SetRotation({DirectX::XMConvertToRadians(22.0f), 0.0f, 0.0f});
        ctx.systems.cameraManager->SetActiveCamera(kEditorCameraName);
        camera_ = &camera;
    }

    if (ctx.rendering.model) {
        levelData_ = LevelDataLoader::Load(kLevelPath, *ctx.rendering.model);
    }

    const std::string objectCount = std::to_string(levelData_.objects.size());
    DebugLog::Get().Write("Editor", "EditorScene", "initialized", "ok",
                          {{"level", levelData_.name},
                           {"objects", objectCount}});
}

void EditorScene::Update() {
    if (!ctx_ || !ctx_->systems.winApp || !camera_) {
        return;
    }

    const int width = ctx_->systems.winApp->GetWidth();
    const int height = ctx_->systems.winApp->GetHeight();
    if (height > 0) {
        camera_->SetAspect(static_cast<float>(width) /
                           static_cast<float>(height));
    }
}

void EditorScene::DrawShadow() {
    if (!ctx_ || !ctx_->rendering.model ||
        !ctx_->rendering.shadowMapRenderer) {
        return;
    }

    ctx_->rendering.model->PreDrawShadow();
    DrawObjectShadows(levelData_.objects);
}

void EditorScene::Draw() {
    if (!ctx_ || !ctx_->rendering.model || !camera_) {
        return;
    }

    ctx_->rendering.model->PreDraw();
    DrawObjects(levelData_.objects, *camera_);
}

void EditorScene::DrawObjects(const std::vector<LevelObject> &objects,
                              const Camera &camera) {
    for (const LevelObject &object : objects) {
        if (object.modelId != UINT32_MAX) {
            ctx_->rendering.model->Draw(object.modelId, object.worldTransform,
                                        camera);
        }

        DrawObjects(object.children, camera);
    }
}

void EditorScene::DrawObjectShadows(const std::vector<LevelObject> &objects) {
    const DirectX::XMFLOAT4X4 &lightViewProjection =
        ctx_->rendering.shadowMapRenderer->GetLightViewProjection();

    for (const LevelObject &object : objects) {
        if (object.modelId != UINT32_MAX) {
            ctx_->rendering.model->DrawShadow(object.modelId,
                                             object.worldTransform,
                                             lightViewProjection);
        }

        DrawObjectShadows(object.children);
    }
}
