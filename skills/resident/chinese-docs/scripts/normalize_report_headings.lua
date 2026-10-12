-- Normalize the canonical Markdown title convention for formal report delivery.
-- A matching document title becomes cover metadata; unmatched body headings survive.

local function heading_text(header)
  return pandoc.utils.stringify(header.content)
end

function Pandoc(doc)
  local title = pandoc.utils.stringify(doc.meta.title or "")
  local first_header_index = nil
  local first_header = nil
  local later_level_one = false
  local later_level_two = false

  for index, block in ipairs(doc.blocks) do
    if block.t == "Header" then
      if first_header == nil then
        first_header_index = index
        first_header = block
      else
        if block.level == 1 then
          later_level_one = true
        elseif block.level == 2 then
          later_level_two = true
        end
      end
    end
  end

  if first_header == nil or first_header.level ~= 1 then
    return doc
  end

  local first_text = heading_text(first_header)
  local matches_metadata = title ~= "" and first_text == title
  local inferred_title = title == "" and not later_level_one and later_level_two
  if not matches_metadata and not inferred_title then
    return doc
  end

  if inferred_title then
    doc.meta.title = pandoc.MetaInlines(first_header.content)
  end
  table.remove(doc.blocks, first_header_index)

  if not later_level_one then
    doc = doc:walk({
      Header = function(header)
        if header.level >= 2 then
          header.level = header.level - 1
        end
        return header
      end,
    })
  end
  return doc
end
