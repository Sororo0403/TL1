#pragma once

#include "Engine.h"

class EditorScene : public BaseScene {
  public:
    void Initialize(const SceneContext &ctx) override;
    void Update() override;
    void DrawShadow() override;
    void Draw() override;

  private:
    void DrawObjects(const std::vector<LevelObject> &objects,
                     const Camera &camera);
    void DrawObjectShadows(const std::vector<LevelObject> &objects);

    LevelData levelData_{};
    Camera *camera_ = nullptr;
};
