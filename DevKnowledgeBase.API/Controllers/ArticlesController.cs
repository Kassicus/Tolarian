using Microsoft.AspNetCore.Mvc;
using DevKnowledgeBase.API.Services;
using DevKnowledgeBase.API.DTOs;

namespace DevKnowledgeBase.API.Controllers;

[ApiController]
[Route("api/[controller]")]
public class ArticlesController : ControllerBase
{
    private readonly ArticleService _articleService;

    public ArticlesController(ArticleService articleService)
    {
        _articleService = articleService;
    }

    // GET: api/articles
    [HttpGet]
    public async Task<ActionResult<List<ArticleDto>>> GetArticles([FromQuery] int page = 1, [FromQuery] int pageSize = 20)
    {
        var articles = await _articleService.GetAllArticlesAsync(page, pageSize);
        return Ok(articles);
    }

    // GET: api/articles/{id}
    [HttpGet("{id:guid}")]
    public async Task<ActionResult<ArticleDto>> GetArticle(Guid id)
    {
        var article = await _articleService.GetArticleByIdAsync(id);
        if (article == null)
            return NotFound(new { message = $"Article with ID {id} not found" });

        return Ok(article);
    }

    // GET: api/articles/slug/{slug}
    [HttpGet("slug/{slug}")]
    public async Task<ActionResult<ArticleDto>> GetArticleBySlug(string slug)
    {
        var article = await _articleService.GetArticleBySlugAsync(slug);
        if (article == null)
            return NotFound(new { message = $"Article with slug '{slug}' not found" });

        return Ok(article);
    }

    // POST: api/articles
    [HttpPost]
    public async Task<ActionResult<ArticleDto>> CreateArticle([FromBody] CreateArticleDto createDto)
    {
        if (!ModelState.IsValid)
            return BadRequest(ModelState);

        var article = await _articleService.CreateArticleAsync(createDto);
        return CreatedAtAction(nameof(GetArticle), new { id = article.Id }, article);
    }

    // PUT: api/articles/{id}
    [HttpPut("{id:guid}")]
    public async Task<ActionResult<ArticleDto>> UpdateArticle(Guid id, [FromBody] UpdateArticleDto updateDto)
    {
        if (!ModelState.IsValid)
            return BadRequest(ModelState);

        var article = await _articleService.UpdateArticleAsync(id, updateDto);
        if (article == null)
            return NotFound(new { message = $"Article with ID {id} not found" });

        return Ok(article);
    }

    // DELETE: api/articles/{id}
    [HttpDelete("{id:guid}")]
    public async Task<ActionResult> DeleteArticle(Guid id)
    {
        var result = await _articleService.DeleteArticleAsync(id);
        if (!result)
            return NotFound(new { message = $"Article with ID {id} not found" });

        return NoContent();
    }
}
